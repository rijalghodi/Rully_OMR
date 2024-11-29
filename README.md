# Rully: AI-Powered Universal Bubble Sheet Grader

Proposed as final project of AI/ML Specialized Bootcamp Dibimbing

- Name: Rijal Ghodi
- Email: rijalgdev@gmail.com
- Github: https://github.com/rijalghodi
- Portfolio: https://zalcode.my.id

<img src="https://t3.ftcdn.net/jpg/03/07/88/98/360_F_307889892_dSTifVpnJZiuq82l1efgXSjcABKAwSlP.jpg" width="600px" height="auto" alt="Bubble Sheet Illustration"/>

## What It is About?

Rully is AI-powered bubble sheet grader capable of accurately and efficiently grading various bubble sheet formats. Leveraging advanced image recognition and machine learning technologies,

## How to Run Locally?

1. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

2. Go to `/api` directory and run the server

   ```bash
   cd api

   uvicorn app:app --reload
   ```

3. Open browser `localhost:10000` to see the API server documentation

## How to Run with Docker?

1. Install docker
2. Go to the root directory of this project
3. Build image
   ```bash
   docker build -t rully .
   ```
4. Run container
   ```bash
   docker run -t rully -p 10000:10000 rully
   ```
5. Open browser `localhost:10000` to see the API server documentation
