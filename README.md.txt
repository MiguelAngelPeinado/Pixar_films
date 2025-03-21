📊 Pixar Films Dashboard:

Welcome to the Pixar Films Dashboard, an interactive data visualization project developed with Python, Streamlit, and Plotly. This dashboard allows users to explore key metrics, financial performance, and critical reception of Pixar movies in an engaging and visually appealing way.

📚 About This Project:
This project was developed as part of a personal learning journey to enhance my skills in data analytics and dashboard creation using Streamlit, Plotly, and Python. It is not intended for commercial or professional use but rather as a showcase piece for my portfolio.


🚀 Features: 

- Key Performance Indicators (KPIs): Quickly view total worldwide box office revenue, most productive year, and most profitable film.

- Interactive Filters: Filter films by release year range and age rating, fully responsive.

- Dynamic Visualizations:
	- Budget vs Profit Margin: Bar chart with interactive filters.
	- Worldwide Box Office vs Budget: Scatter plot showing correlations.
	- Critics Score Evolution: Line chart comparing Rotten Tomatoes and Metacritic scores.
	- Critics vs Box Office Analysis (in Expander): Explore additional insights with trendlines.

- Detailed Film Selector: Select any Pixar film and view detailed stats.

📂 Project Structure

	📁 Data
	 └── pixar_clean_streamlit.csv
	📄 app.py
	📄 README.md

🛠️ Tech:

- Python
- Streamlit
- Plotly (Graph Objects & Express)
- Pandas

🌐 Deployment:
This project can be deployed easily:

1.- Clone the Repo

Clone the entire repository and navigate to the Pixar Films project folder:

```bash
git clone https://github.com/MiguelAngelPeinado/Projects.git
cd Projects/tidytuesday_challenges/Pixar_films

2.- Install dependencies:
	pip install -r requirements.txt

3.- Run locally:
	streamlit run app.py

4.- Deploy on Streamlit Community Cloud, Heroku, or any platform of your choice.


📜 License & Credits:
Dataset sourced and cleaned from public domain/TidyTuesday.
Pixar, Disney logos, and references are for educational purposes only. © Disney / Pixar.
