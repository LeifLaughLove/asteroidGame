# 🪐 Asteroid Game

A classic arcade-style shooter inspired by *Asteroids*, built with Python and Pygame. Features a live Flask + PostgreSQL-powered leaderboard.

---

## 🎮 Features

- Classic arcade-style gameplay
- Increasing difficulty based on score
- One power-up available (Speed Boost)
- Live leaderboard using a separate Flask + PostgreSQL server
- Small menu screen with Start and Leaderboard buttons

---

## 🛠️ Tech Used

- **Python 3**
- **Pygame**
- **Flask** (for leaderboard API)
- **PostgreSQL** (for storing scores)
- **Git / GitHub**

---

## 🚀 How to Run the Game

### 1. Clone the repo
```bash
git clone https://github.com/LeifLaughLove/asteroidGame.git
cd asteroidGame
```

### 2. Setup virtual environment

  (WSL/Linux)
  ```
    python3 -m venv venv
    source venv/bin/activate
  ```
    
  (For Windows)
  ```
    python -m venv venv
    venv\Scripts\activate
  ```

### 3. Install requirements 
  ```
  pip install -r requirements.txt
  ```
### 4. Leaderboard (OPTIONAL)

```
THE GAME WILL RUN WITHOUT SETTING UP THE LEADERBOARD
```

  
 To make the leaderboard live a .env needs to be made in asteroidGame and a SERVER_URL needs to be placed there (SERVER_URL=https://eample.com)
 
 - CLONE OR DOWNLOAD THE LEADERBOARD SERVER -- https://github.com/LeifLaughLove/leaderboardServer
 - Deploy leaderboardServer to render.com
 - Create a new **Web Service**
 - connect it to your "leaderboardServer" repo
 - in render settings add an environments variable
   ```
    DATABASE_URL=your_postgres1l_connection_string
   ```
 - start the service and copy the public Render URL (`https://your-leaderboard-server.onrender.com`)

   **Update SERVER_URL in your 'asteroidGame' project**

 - in asteroidGame folder create a new .env file, add the following line
   ```
         SERVER_URL=https://example.com
   ```

### 5. Run The Game
-everything should work smoothly now


  
