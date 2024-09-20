# MLB_Bet

The aim is to leverage historical MLB data to create predictive models for two key statistics:
Pitcher Strikeouts (K) and Batter Hits (H)

This project aims to apply machine learning techniques to predict MLB player performance, specifically focusing on pitcher strikeouts and batter hits. We use historical player data and live over-under odds from sportsbooks in order to create a database that is easy to use for machine learning models. The data is processed, cleaned, and enhanced with additional features such as trends using a fully automated pipeline.

Data Sources:
**PyBaseball API**: This API is utilized to gather historical player performance data for pitchers and batters, including game-level statistics such as strikeouts, hits, innings pitched, plate appearances, etc.
**mlb_bet_scraper**: A custom web scraper pulls daily over-under betting odds for pitcher strikeouts and batter hits from multiple sportsbooks.
