"""
Simple AI Chat Component - Works without external API dependencies
Provides intelligent data analysis and Q&A capabilities
Enhanced to handle all data sources and answer any question
"""

import streamlit as st
import pandas as pd
import re
from datetime import datetime
import numpy as np


def simple_ai_chat(
    title="AI Assistant", context_df=None, role_hint=None, unmatching_df=None
):
    """
    Simple AI chat that works without external APIs.
    Provides intelligent data analysis based on the context DataFrame.

    Args:
        title: Title for the chat interface
        context_df: Main combined DataFrame (database + matching + manual)
        role_hint: Hint about the data type (cyber_incident, it_ticket, dataset)
        unmatching_df: Unmatching uploaded data (separate DataFrame)
    """

    # Initialize chat history
    chat_key = f"simple_ai_chat_{role_hint or 'default'}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    # CSS Styling
    st.markdown(
        """
    <style>
    .ai-chat-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #7b2ff7;
        box-shadow: 0 0 30px rgba(123, 47, 247, 0.3);
        margin: 20px 0;
    }
    
    .ai-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 28px;
        color: #ff33ff;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #ff33ff;
    }
    
    .chat-message {
        padding: 12px 18px;
        margin: 10px 0;
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
        margin-left: auto;
        margin-right: 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    
    .ai-message {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        color: white;
        margin-left: 0;
        margin-right: auto;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    }
    
    .chat-history {
        max-height: 400px;
        overflow-y: auto;
        padding: 15px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Title
    st.markdown(
        f'<div class="ai-chat-container"><div class="ai-title">🤖 {title}</div>',
        unsafe_allow_html=True,
    )

    # Welcome message
    if len(st.session_state[chat_key]) == 0:
        welcome_msg = "Hello! I'm your AI assistant. I can help you analyze your data, answer questions, and provide insights. Try asking me about your data!"
        st.session_state[chat_key].append({"role": "assistant", "content": welcome_msg})

    # Display chat history
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for msg in st.session_state[chat_key]:
        css_class = "user-message" if msg["role"] == "user" else "ai-message"
        st.markdown(
            f'<div class="chat-message {css_class}">{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # User input
    user_input = st.chat_input(
        "Ask me anything about your data...", key=f"simple_ai_input_{role_hint}"
    )

    if user_input:
        # Add user message
        st.session_state[chat_key].append({"role": "user", "content": user_input})

        # Generate AI response
        ai_response = generate_response(
            user_input, context_df, role_hint, unmatching_df
        )

        # Add AI response
        st.session_state[chat_key].append({"role": "assistant", "content": ai_response})

        # Rerun to show new messages
        st.rerun()

    # Clear chat button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state[chat_key] = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def generate_response(user_input, context_df=None, role_hint=None, unmatching_df=None):
    """
    Generate intelligent response based on user input and all available data.

    This function intelligently handles ANY question about the data by:
    1. Combining all data sources (context_df + unmatching_df)
    2. Dynamically detecting columns and data types
    3. Parsing questions to extract intent, columns, values, and filters
    4. Providing comprehensive answers
    """

    # Combine all data sources
    all_data = []
    data_sources = []
    column_info = {}  # Track which columns come from which source

    if context_df is not None and not context_df.empty:
        all_data.append(context_df.copy())
        data_sources.append("main database")
        # Track columns from main database
        for col in context_df.columns:
            column_info[col] = "main database"

    if unmatching_df is not None and not unmatching_df.empty:
        all_data.append(unmatching_df.copy())
        data_sources.append("unmatching uploaded data")
        # Track columns from unmatching data
        for col in unmatching_df.columns:
            if col not in column_info:
                column_info[col] = "unmatching uploaded data"
            else:
                column_info[col] = "both sources"

    if not all_data:
        return "I don't have access to any data right now. Please make sure data is loaded in the dashboard."

    # Combine all DataFrames - handle different column structures
    if len(all_data) > 1:
        # When combining DataFrames with different columns, use outer join
        # This preserves all columns from both DataFrames
        try:
            combined_df = pd.concat(all_data, ignore_index=True, sort=False)
            # Fill NaN values that result from missing columns with appropriate defaults
            # For object columns, use empty string; for numeric, use NaN (which we'll handle)
            for col in combined_df.columns:
                if combined_df[col].dtype == "object":
                    combined_df[col] = combined_df[col].fillna("")
        except Exception as e:
            # If concat fails, try alternative approach
            # Create a union of all columns
            all_columns = set()
            for df in all_data:
                all_columns.update(df.columns)

            # Reindex each DataFrame to include all columns
            dfs_aligned = []
            for df in all_data:
                df_aligned = df.reindex(columns=all_columns)
                dfs_aligned.append(df_aligned)

            combined_df = pd.concat(dfs_aligned, ignore_index=True, sort=False)
            # Fill NaN for object columns
            for col in combined_df.columns:
                if combined_df[col].dtype == "object":
                    combined_df[col] = combined_df[col].fillna("")
    else:
        combined_df = all_data[0]

    user_input_lower = user_input.lower().strip()

    # Get all available columns
    available_columns = list(combined_df.columns)

    # Comprehensive question analysis
    response = analyze_and_answer(
        user_input_lower, combined_df, available_columns, role_hint, data_sources
    )

    return response


def analyze_and_answer(user_input, df, columns, role_hint, data_sources):
    """Comprehensive question analysis and answer generation."""

    # Normalize column names for matching
    col_map = {col.lower().strip(): col for col in columns}

    # Extract potential column names from user input - use word boundaries for accuracy
    mentioned_columns = []
    for col_key, col_name in col_map.items():
        # Use word boundaries to avoid partial matches (e.g., "status" shouldn't match "statistics")
        col_pattern = r"\b" + re.escape(col_key) + r"\b"
        if re.search(col_pattern, user_input):
            mentioned_columns.append(col_name)

    # Detect question type and intent
    question_type = detect_question_type(user_input, df, columns)

    # Handle different question types
    if question_type == "count":
        return handle_comprehensive_count(
            user_input, df, columns, mentioned_columns, role_hint, data_sources
        )
    elif question_type == "statistics":
        return handle_comprehensive_statistics(
            user_input, df, columns, mentioned_columns, role_hint
        )
    elif question_type == "search":
        return handle_comprehensive_search(
            user_input, df, columns, mentioned_columns, role_hint
        )
    elif question_type == "filter":
        return handle_comprehensive_filter(
            user_input, df, columns, mentioned_columns, role_hint
        )
    elif question_type == "comparison":
        return handle_comprehensive_comparison(
            user_input, df, columns, mentioned_columns, role_hint
        )
    elif question_type == "trend":
        return handle_comprehensive_trend(
            user_input, df, columns, mentioned_columns, role_hint
        )
    elif question_type == "value":
        return handle_value_query(user_input, df, columns, mentioned_columns, role_hint)
    elif question_type == "list":
        return handle_list_query(user_input, df, columns, mentioned_columns, role_hint)
    elif question_type == "summary":
        return handle_comprehensive_summary(df, columns, role_hint, data_sources)
    else:
        return handle_intelligent_fallback(
            user_input, df, columns, role_hint, data_sources
        )


def detect_question_type(user_input, df, columns):
    """Detect the type of question being asked."""

    count_words = ["how many", "count", "total", "number of", "quantity"]
    stats_words = [
        "average",
        "mean",
        "median",
        "min",
        "max",
        "sum",
        "statistics",
        "stats",
        "avg",
    ]
    search_words = ["find", "search", "show", "display", "get"]
    filter_words = ["where", "which", "what", "who", "when", "with", "having"]
    compare_words = [
        "compare",
        "difference",
        "vs",
        "versus",
        "more than",
        "less than",
        "greater",
        "smaller",
    ]
    trend_words = [
        "trend",
        "over time",
        "recent",
        "latest",
        "oldest",
        "newest",
        "earliest",
        "last",
    ]
    value_words = ["value", "what is", "tell me", "give me"]
    list_words = ["list", "all", "every", "each"]
    summary_words = ["summary", "overview", "tell me about", "describe"]

    if any(word in user_input for word in count_words):
        return "count"
    elif any(word in user_input for word in stats_words):
        return "statistics"
    elif any(word in user_input for word in search_words):
        return "search"
    elif any(word in user_input for word in filter_words):
        return "filter"
    elif any(word in user_input for word in compare_words):
        return "comparison"
    elif any(word in user_input for word in trend_words):
        return "trend"
    elif any(word in user_input for word in value_words):
        return "value"
    elif any(word in user_input for word in list_words):
        return "list"
    elif any(word in user_input for word in summary_words):
        return "summary"
    else:
        return "general"


def handle_comprehensive_count(
    user_input, df, columns, mentioned_cols, role_hint, data_sources
):
    """Handle count questions comprehensively."""

    response = ""
    total_records = len(df)

    # Check for specific column mentions
    if mentioned_cols:
        for col in mentioned_cols:
            if col in df.columns:
                # Count unique values or specific values
                if "unique" in user_input or "different" in user_input:
                    unique_count = df[col].nunique()
                    response += f"📊 **Unique {col} values:** {unique_count}\n\n"
                else:
                    # Value counts - only count non-null values
                    non_null_data = df[col].dropna()
                    if len(non_null_data) > 0:
                        value_counts = non_null_data.value_counts()
                        if len(value_counts) <= 20:  # Only show if reasonable number
                            response += f"📊 **Count by {col}:**\n\n"
                            for val, count in value_counts.items():
                                pct = (count / total_records) * 100
                                response += f"- **{val}:** {count} ({pct:.1f}%)\n"
                            response += "\n"

    # Check for specific value mentions in the question - more precise matching
    # Extract column-value pairs more accurately
    for col in columns:
        col_lower = col.lower()
        # Only check if column name appears as a word (not substring)
        col_pattern = r"\b" + re.escape(col_lower) + r"\b"
        if re.search(col_pattern, user_input):
            # Look for common values that might be related to this column
            for val in [
                "critical",
                "high",
                "medium",
                "low",
                "open",
                "closed",
                "resolved",
                "pending",
                "active",
                "inactive",
            ]:
                # Check if value appears near the column name or as a standalone word
                val_pattern = r"\b" + re.escape(val) + r"\b"
                if re.search(val_pattern, user_input):
                    if col in df.columns:
                        # More accurate matching - handle NaN values properly
                        mask = df[col].notna()
                        if mask.any():
                            count = (
                                df.loc[mask, col].astype(str).str.lower().str.strip()
                                == val
                            ).sum()
                            if count > 0:
                                response += (
                                    f"📊 **{col} = '{val.title()}':** {count}\n\n"
                                )
                                break  # Only count once per column

    # If no specific answer found, provide general counts
    if not response:
        response = f"📊 **Total Records:** {total_records}\n\n"

        # Show counts for common categorical columns (including unmatching data columns)
        categorical_cols = [
            col
            for col in columns
            if df[col].dtype == "object" and df[col].nunique() <= 20
        ]
        # Prioritize columns with more non-null values (main data columns first)
        categorical_cols.sort(key=lambda x: df[x].notna().sum(), reverse=True)

        for col in categorical_cols[:7]:  # Increased limit to show more columns
            non_null_data = df[col].dropna()
            if len(non_null_data) > 0:
                value_counts = non_null_data.value_counts().head(10)
                if len(value_counts) > 0:
                    response += f"**{col} Distribution:**\n"
                    for val, count in value_counts.items():
                        pct = (count / total_records) * 100
                        response += f"- {val}: {count} ({pct:.1f}%)\n"
                    response += "\n"

    # Add data source info
    if len(data_sources) > 1:
        response += f"\n*Data from: {', '.join(data_sources)}*\n"

    return response if response else f"Found {total_records} records in total."


def handle_comprehensive_statistics(user_input, df, columns, mentioned_cols, role_hint):
    """Handle statistics questions comprehensively."""

    response = "📈 **Statistical Analysis:**\n\n"

    # Find numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Check for specific column mentions
    analyzed_cols = []
    if mentioned_cols:
        for col in mentioned_cols:
            if col in numeric_cols:
                analyzed_cols.append(col)

    # If no specific column, analyze all numeric columns (up to 5)
    if not analyzed_cols:
        analyzed_cols = numeric_cols[:5]

    if analyzed_cols:
        for col in analyzed_cols:
            # Only calculate stats on non-null values
            col_data = df[col].dropna()
            if len(col_data) > 0:
                stats = col_data.describe()
                response += f"**{col} Statistics:**\n"
                response += f"- Count: {int(stats['count'])}\n"
                if "mean" in stats:
                    response += f"- Mean: {stats['mean']:.2f}\n"
                if "50%" in stats:
                    response += f"- Median: {stats['50%']:.2f}\n"
                if "min" in stats:
                    response += f"- Min: {stats['min']:.2f}\n"
                if "max" in stats:
                    response += f"- Max: {stats['max']:.2f}\n"
                if "std" in stats and pd.notna(stats["std"]):
                    response += f"- Std Dev: {stats['std']:.2f}\n"
                response += "\n"
    else:
        response += "No numeric columns found for statistical analysis.\n"
        # Show categorical statistics instead
        categorical_cols = [
            col
            for col in columns
            if df[col].dtype == "object" and df[col].nunique() <= 20
        ]
        for col in categorical_cols[:3]:
            non_null_data = df[col].dropna()
            if len(non_null_data) > 0:
                value_counts = non_null_data.value_counts()
                response += f"**{col} Distribution:**\n"
                for val, count in value_counts.head(5).items():
                    pct = (count / len(df)) * 100
                    response += f"- {val}: {count} ({pct:.1f}%)\n"
                response += "\n"

    return response


def handle_comprehensive_search(user_input, df, columns, mentioned_cols, role_hint):
    """Handle search questions comprehensively."""

    # Extract search terms
    search_terms = re.findall(r"\b\w+\b", user_input.lower())
    # Remove common stop words
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "should",
        "could",
        "may",
        "might",
        "must",
        "can",
        "find",
        "show",
        "search",
        "get",
        "display",
    }
    search_terms = [
        term for term in search_terms if term not in stop_words and len(term) > 2
    ]

    if not search_terms:
        return "Please provide specific search terms. For example: 'Find incidents with high severity'"

    # Search across all text columns (including unmatching data columns)
    text_columns = [col for col in columns if df[col].dtype == "object"]
    matches = pd.DataFrame()

    for col in text_columns:
        # Search in this column, handling NaN values properly
        try:
            mask = (
                df[col]
                .astype(str)
                .str.lower()
                .str.contains("|".join(search_terms), case=False, na=False, regex=True)
            )
            if mask.any():
                # Get matching rows
                matching_rows = df[mask].copy()
                matches = pd.concat([matches, matching_rows], ignore_index=True)
        except Exception:
            # Skip columns that can't be searched (e.g., complex types)
            continue

    # Remove duplicates (based on all columns)
    if not matches.empty:
        matches = matches.drop_duplicates()

    if not matches.empty:
        response = f"🔍 **Found {len(matches)} matching records:**\n\n"

        # Show key information for each match (limit to 10)
        for idx, row in matches.head(10).iterrows():
            # Show primary key or first few columns
            key_info = []
            for col in columns[:5]:  # Show first 5 columns
                val = row.get(col, "N/A")
                if pd.notna(val) and str(val).strip():
                    key_info.append(f"{col}: {val}")

            response += f"**Record {idx + 1}:**\n"
            response += " - ".join(key_info[:3]) + "\n\n"

        if len(matches) > 10:
            response += f"... and {len(matches) - 10} more results.\n"
    else:
        response = f"❌ No records found matching: {', '.join(search_terms)}\n\n"
        response += (
            "Try different search terms or ask about specific columns or values."
        )

    return response


def handle_comprehensive_filter(user_input, df, columns, mentioned_cols, role_hint):
    """Handle filter questions comprehensively."""

    # Try to extract column-value pairs
    filtered_df = df.copy()
    filters_applied = []

    # Look for column-value patterns - more precise matching
    for col in columns:
        col_lower = col.lower()
        # Use word boundaries for column matching
        col_pattern = r"\b" + re.escape(col_lower) + r"\b"
        if re.search(col_pattern, user_input):
            # Try to find values mentioned
            for val in [
                "critical",
                "high",
                "medium",
                "low",
                "open",
                "closed",
                "resolved",
                "pending",
                "active",
                "inactive",
            ]:
                # Use word boundaries for value matching
                val_pattern = r"\b" + re.escape(val) + r"\b"
                if re.search(val_pattern, user_input):
                    if col in df.columns:
                        # Handle NaN values properly
                        mask = df[col].notna()
                        if mask.any():
                            value_mask = (
                                df.loc[mask, col].astype(str).str.lower().str.strip()
                                == val
                            )
                            final_mask = mask.copy()
                            final_mask.loc[mask] = value_mask
                            if final_mask.any():
                                filtered_df = filtered_df[final_mask]
                                filters_applied.append(f"{col} = {val}")
                                break  # Only apply one filter per column

    # Also check for numeric comparisons
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        col_lower = col.lower()
        # Use word boundaries for column matching
        col_pattern = r"\b" + re.escape(col_lower) + r"\b"
        if re.search(col_pattern, user_input):
            # Look for comparison operators
            if (
                "greater than" in user_input
                or "more than" in user_input
                or ">" in user_input
            ):
                # Extract number
                numbers = re.findall(r"\d+\.?\d*", user_input)
                if numbers:
                    threshold = float(numbers[0])
                    # Handle NaN values - only filter non-null values
                    numeric_mask = df[col].notna() & (df[col] > threshold)
                    if numeric_mask.any():
                        filtered_df = filtered_df[numeric_mask]
                        filters_applied.append(f"{col} > {threshold}")
                        break  # Only apply one numeric filter per column
            elif (
                "less than" in user_input
                or "smaller than" in user_input
                or "<" in user_input
            ):
                numbers = re.findall(r"\d+\.?\d*", user_input)
                if numbers:
                    threshold = float(numbers[0])
                    # Handle NaN values - only filter non-null values
                    numeric_mask = df[col].notna() & (df[col] < threshold)
                    if numeric_mask.any():
                        filtered_df = filtered_df[numeric_mask]
                        filters_applied.append(f"{col} < {threshold}")
                        break  # Only apply one numeric filter per column

    if filters_applied:
        response = f"🔍 **Filtered Results ({len(filtered_df)} records):**\n\n"
        response += f"Filters applied: {', '.join(filters_applied)}\n\n"

        # Show sample results
        for idx, row in filtered_df.head(10).iterrows():
            key_info = []
            for col in columns[:4]:
                val = row.get(col, "N/A")
                if pd.notna(val) and str(val).strip():
                    key_info.append(f"{col}: {val}")
            response += f"**Record {idx + 1}:** {' | '.join(key_info[:3])}\n"

        if len(filtered_df) > 10:
            response += f"\n... and {len(filtered_df) - 10} more records.\n"
    else:
        response = handle_comprehensive_search(
            user_input, df, columns, mentioned_cols, role_hint
        )

    return response


def handle_comprehensive_comparison(user_input, df, columns, mentioned_cols, role_hint):
    """Handle comparison questions comprehensively."""

    response = "📊 **Comparison Analysis:**\n\n"

    # Find categorical columns for comparison
    categorical_cols = [
        col for col in columns if df[col].dtype == "object" and df[col].nunique() <= 20
    ]

    if mentioned_cols:
        categorical_cols = [col for col in mentioned_cols if col in categorical_cols]

    if categorical_cols:
        for col in categorical_cols[:3]:  # Limit to 3 columns
            # Only count non-null values
            non_null_data = df[col].dropna()
            if len(non_null_data) > 0:
                value_counts = non_null_data.value_counts()
                response += f"**{col} Comparison:**\n"
                total = len(df)
                for val, count in value_counts.items():
                    pct = (count / total) * 100
                    response += f"- **{val}:** {count} ({pct:.1f}%)\n"
                response += "\n"
    else:
        # Compare numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            response += "**Numeric Column Comparisons:**\n"
            for col in numeric_cols[:3]:
                response += f"- **{col}:** Min={df[col].min():.2f}, Max={df[col].max():.2f}, Avg={df[col].mean():.2f}\n"
            response += "\n"

    return response


def handle_comprehensive_trend(user_input, df, columns, mentioned_cols, role_hint):
    """Handle trend/time-based questions comprehensively."""

    # Find date columns
    date_cols = []
    for col in columns:
        if any(
            keyword in col.lower()
            for keyword in ["date", "time", "timestamp", "created", "updated"]
        ):
            date_cols.append(col)

    if not date_cols:
        # Try to detect date columns by content
        for col in columns:
            try:
                pd.to_datetime(df[col].head(10), errors="raise")
                date_cols.append(col)
            except:
                pass

    if date_cols:
        date_col = date_cols[0]
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df_sorted = df.sort_values(date_col, na_position="last")

        response = "📈 **Trend Analysis:**\n\n"

        if "recent" in user_input or "latest" in user_input or "newest" in user_input:
            latest = df_sorted.tail(10)
            response += "**Most Recent Records:**\n\n"
            for idx, row in latest.iterrows():
                key_info = []
                for col in columns[:4]:
                    val = row.get(col, "N/A")
                    if pd.notna(val) and str(val).strip():
                        key_info.append(f"{col}: {val}")
                response += f"- {' | '.join(key_info[:3])}\n"

        elif "oldest" in user_input or "earliest" in user_input:
            oldest = df_sorted.head(10)
            response += "**Oldest Records:**\n\n"
            for idx, row in oldest.iterrows():
                key_info = []
                for col in columns[:4]:
                    val = row.get(col, "N/A")
                    if pd.notna(val) and str(val).strip():
                        key_info.append(f"{col}: {val}")
                response += f"- {' | '.join(key_info[:3])}\n"
        else:
            # General trend
            response += f"**Date Range:** {df_sorted[date_col].min()} to {df_sorted[date_col].max()}\n\n"
            response += f"**Total Records:** {len(df)}\n"
            response += f"**Records per Period:**\n"
            # Group by period if possible
            try:
                df_sorted["period"] = df_sorted[date_col].dt.to_period("M")
                period_counts = df_sorted["period"].value_counts().sort_index()
                for period, count in period_counts.tail(6).items():
                    response += f"- {period}: {count} records\n"
            except:
                pass
    else:
        response = "No date/time columns found for trend analysis."

    return response


def handle_value_query(user_input, df, columns, mentioned_cols, role_hint):
    """Handle specific value queries."""

    response = "📋 **Value Query Results:**\n\n"

    # Try to find specific values mentioned - use word boundaries
    for col in columns:
        col_lower = col.lower()
        col_pattern = r"\b" + re.escape(col_lower) + r"\b"
        if re.search(col_pattern, user_input):
            # Show unique values or sample values
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) > 0:
                if len(unique_vals) <= 20:
                    response += f"**{col} values:**\n"
                    for val in unique_vals[:15]:
                        response += f"- {val}\n"
                    if len(unique_vals) > 15:
                        response += f"... and {len(unique_vals) - 15} more\n"
                    response += "\n"
                else:
                    response += f"**{col}:** {len(unique_vals)} unique values\n"
                    response += f"Sample values: {', '.join([str(v) for v in unique_vals[:10]])}\n\n"

    if "value" in response.lower() and len(response.split("\n")) < 5:
        # Fallback to search
        return handle_comprehensive_search(
            user_input, df, columns, mentioned_cols, role_hint
        )

    return response


def handle_list_query(user_input, df, columns, mentioned_cols, role_hint):
    """Handle list/all queries."""

    response = f"📋 **All Records ({len(df)} total):**\n\n"

    # Limit to reasonable number
    display_limit = 20
    for idx, row in df.head(display_limit).iterrows():
        key_info = []
        for col in columns[:4]:
            val = row.get(col, "N/A")
            if pd.notna(val) and str(val).strip():
                key_info.append(f"{col}: {val}")
        response += f"**Record {idx + 1}:** {' | '.join(key_info[:3])}\n"

    if len(df) > display_limit:
        response += f"\n... and {len(df) - display_limit} more records.\n"

    return response


def handle_comprehensive_summary(df, columns, role_hint, data_sources):
    """Handle summary/overview questions comprehensively."""

    response = "📋 **Comprehensive Data Summary:**\n\n"
    response += f"- **Total Records:** {len(df)}\n"
    response += f"- **Total Columns:** {len(columns)}\n"

    if len(data_sources) > 1:
        response += f"- **Data Sources:** {', '.join(data_sources)}\n"

    response += "\n**Column Information:**\n"

    # Show column types and sample info - include all columns to show unmatching data columns
    for col in columns[
        :20
    ]:  # Increased limit to show more columns (including unmatching)
        dtype = str(df[col].dtype)
        non_null = df[col].notna().sum()
        unique = df[col].nunique()
        # Indicate if column is from unmatching data (has many NaN values in main data context)
        pct_null = (df[col].isna().sum() / len(df)) * 100
        source_hint = ""
        if pct_null > 50 and len(data_sources) > 1:
            source_hint = " (mostly from unmatching data)"
        response += f"- **{col}:** {dtype}, {non_null} non-null, {unique} unique values{source_hint}\n"

    if len(columns) > 20:
        response += f"\n... and {len(columns) - 20} more columns.\n"

    # Show key statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        response += "\n**Numeric Column Statistics:**\n"
        for col in numeric_cols[:5]:
            response += f"- **{col}:** Min={df[col].min():.2f}, Max={df[col].max():.2f}, Avg={df[col].mean():.2f}\n"

    # Show value distributions for categorical columns
    categorical_cols = [
        col for col in columns if df[col].dtype == "object" and df[col].nunique() <= 10
    ]
    if categorical_cols:
        response += "\n**Categorical Distributions:**\n"
        for col in categorical_cols[:3]:
            top_values = df[col].value_counts().head(3)
            response += f"- **{col}:** {', '.join([f'{k}({v})' for k, v in top_values.items()])}\n"

    return response


def handle_intelligent_fallback(user_input, df, columns, role_hint, data_sources):
    """Intelligent fallback that tries to answer any question."""

    # Try to extract any column or value mentions
    mentioned_cols = []
    for col in columns:
        if col.lower() in user_input.lower():
            mentioned_cols.append(col)

    if mentioned_cols:
        # Try to provide information about mentioned columns
        response = f"📊 **Information about mentioned columns:**\n\n"
        for col in mentioned_cols[:5]:
            if col in df.columns:
                unique_count = df[col].nunique()
                non_null = df[col].notna().sum()
                response += f"**{col}:**\n"
                response += f"- Unique values: {unique_count}\n"
                response += f"- Non-null records: {non_null}\n"

                if df[col].dtype in ["int64", "float64"]:
                    response += f"- Min: {df[col].min()}, Max: {df[col].max()}, Avg: {df[col].mean():.2f}\n"
                else:
                    top_values = df[col].value_counts().head(5)
                    response += f"- Top values: {', '.join([f'{k}({v})' for k, v in top_values.items()])}\n"
                response += "\n"
    else:
        # General help
        response = "💡 **I can help you with:**\n\n"
        response += "• **Counts:** 'How many records are there?'\n"
        response += "• **Statistics:** 'What's the average of [column]?'\n"
        response += "• **Search:** 'Find records with [value]'\n"
        response += "• **Filters:** 'Show records where [column] = [value]'\n"
        response += "• **Comparisons:** 'Compare [column] values'\n"
        response += "• **Trends:** 'Show me recent records'\n"
        response += "• **Lists:** 'List all [column] values'\n"
        response += "• **Summaries:** 'Give me an overview'\n\n"
        response += f"**Available columns:** {', '.join(columns[:10])}"
        if len(columns) > 10:
            response += f" ... and {len(columns) - 10} more"
        response += f"\n\n**Total records:** {len(df)}"
        if len(data_sources) > 1:
            response += f"\n**Data sources:** {', '.join(data_sources)}"

    return response
