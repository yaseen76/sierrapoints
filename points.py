import streamlit as st
import pandas as pd
import csv
import io

st.set_page_config(layout="wide")

def load_data(file):
    data = []
    total_points = 0
    
    csv_reader = csv.DictReader(io.StringIO(file.getvalue().decode('utf-8')), delimiter='\t')
    for row in csv_reader:
        try:
            trade_type = row['Trade Type']
            entry_price = float(row['Entry Price'])
            exit_price = float(row['Exit Price'])
            
            if trade_type == 'Long':
                points = exit_price - entry_price
            elif trade_type == 'Short':
                points = entry_price - exit_price
            else:
                continue
            
            total_points += points
            data.append([trade_type, entry_price, exit_price, points])
        except (ValueError, KeyError):
            continue

    return data, total_points

def main():
    st.title("Trade Points Summary")

    uploaded_file = st.file_uploader("Choose a TSV file", type="txt")
    
    if uploaded_file is not None:
        data, total_points = load_data(uploaded_file)

        if not data:
            st.error("No valid data to display.")
        else:
            df = pd.DataFrame(data, columns=['Trade Type', 'Entry', 'Exit', 'Points'])

            def color_points(val):
                color = 'green' if val > 0 else 'red' if val < 0 else 'black'
                return f'color: {color}'


            styled_df = df.style.applymap(color_points, subset=['Points'])

            # Display stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Points", f"{total_points:.2f}")
            with col2:
                st.metric("Number of Trades", len(data))
            with col3:
                st.metric("Average Points per Trade", f"{total_points / len(data):.2f}")
            st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()