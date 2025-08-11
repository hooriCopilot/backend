# Career Assessment & Password Manager Backend

## How to Run

1. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment variables (optional but recommended)**
    - Create a `.env` file in the backend directory:
      ```
      DATABASE_URL=sqlite:///./app.db
      JWT_SECRET=your_jwt_secret
      FERNET_KEY=your_fernet_key
      ```
    - Generate a Fernet key:
      ```python
      from cryptography.fernet import Fernet
      print(Fernet.generate_key().decode())
      ```
    - Paste the result as your `FERNET_KEY`.

4. **Run the server**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 5000 --reload
    ```

5. **Test**
    - Visit [http://localhost:5000/docs](http://localhost:5000/docs) for the Swagger UI.

---

## Folder Structure

```
backend/
│-- api/
│-- core/
│-- models/
│-- schemas/
│-- venv/
│-- main.py
│-- requirements.txt
│-- README.md
│-- ...
```

---

MIT License