import streamlit as st
import json
import os

LIBRARY_FILE = "library.txt"

# Load the library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                st.warning("Could not decode library file. Starting with an empty library.")
    return []

# Save the library to file
def save_library(library):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file, indent=4)

# Display books in formatted way
def display_books(books):
    if not books:
        st.info("No books to display.")
    for i, book in enumerate(books, start=1):
        status = "✅ Read" if book['read'] else "📖 Unread"
        st.markdown(f"**{i}. {book['title']}** by {book['author']} ({book['year']}) - *{book['genre']}* - {status}")

# Main App
def main():
    st.title("📚 Personal Library Manager")

    if "library" not in st.session_state:
        st.session_state.library = load_library()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["➕ Add Book", "❌ Remove Book", "🔍 Search", "📘 All Books", "📊 Statistics"])

    with tab1:
        st.header("Add a New Book")
        with st.form("add_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
            genre = st.text_input("Genre")
            read = st.selectbox("Have you read this book?", ["No", "Yes"])
            submitted = st.form_submit_button("Add Book")

            if submitted:
                new_book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": True if read == "Yes" else False
                }
                st.session_state.library.append(new_book)
                save_library(st.session_state.library)
                st.success("Book added successfully!")

    with tab2:
        st.header("Remove a Book")
        titles = [book['title'] for book in st.session_state.library]
        if titles:
            selected = st.selectbox("Select a book to remove", titles)
            if st.button("Remove Book"):
                st.session_state.library = [book for book in st.session_state.library if book['title'] != selected]
                save_library(st.session_state.library)
                st.success("Book removed!")
        else:
            st.info("No books available to remove.")

    with tab3:
        st.header("Search Books")
        search_by = st.radio("Search by", ["Title", "Author"])
        keyword = st.text_input("Enter search term")
        if st.button("Search"):
            if search_by == "Title":
                results = [book for book in st.session_state.library if keyword.lower() in book['title'].lower()]
            else:
                results = [book for book in st.session_state.library if keyword.lower() in book['author'].lower()]
            display_books(results)

    with tab4:
        st.header("All Books in Library")
        display_books(st.session_state.library)

    with tab5:
        st.header("Library Statistics")
        total = len(st.session_state.library)
        read = sum(1 for book in st.session_state.library if book['read'])
        percent = (read / total) * 100 if total else 0
        st.metric("📚 Total Books", total)
        st.metric("✅ Read Percentage", f"{percent:.1f}%")

if __name__ == "__main__":
    main()
