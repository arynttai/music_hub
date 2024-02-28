import psycopg2
from fastapi import FastAPI, Request, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import psycopg2.extras
import hashlib
from fastapi import Form

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# css, js, images
app.mount("/static", StaticFiles(directory="static"), name="static")

# html странички
templates = Jinja2Templates(directory="templates")

# бд
def get_db():
    conn = psycopg2.connect(
        dbname="musichub",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    return conn


pages = ["rusdark", "rusdarkaccount", "rusdarkc1", "rusdarkc2", "rusdarkc3", "rusdarkc4",
         "rusdarkc5", "rusdarkc6", "rusdarkcustomers", "rusdarkevents", "rusdarkevform",
         "rusdarkg1", "rusdarkg2", "rusdarkg3", "rusdarkg4", "rusdarkg5", "rusdarkg6",
         "rusdarkmain", "rusdarkmusform", "rusdarkmusicians",
         "rusdarkquestions", "rusdarksignin",
         "ruslight", "ruslightaccount", "ruslightc1", "ruslightc2", "ruslightc3",
         "ruslightc4", "ruslightc5", "ruslightc6", "ruslightcustomers", "ruslightevents", "ruslightevform",
         "ruslightg1", "ruslightg2", "ruslightg3", "ruslightg4",
         "ruslightg5", "ruslightg6", "ruslightmain", "ruslightmusform", "ruslightmusicians",
         "ruslightquestions", "ruslightsignin",
         "kazdark", "kazdarkaccount", 
         "kazdarkc1", "kazdarkc2", "kazdarkc3", "kazdarkc4",
         "kazdarkc5", "kazdarkc6", "kazdarkcustomers", "kazdarkevents",
         "kazdarkg1", "kazdarkg2", "kazdarkg3", "kazdarkg4", "kazdarkg5", "kazdarkg6",
         "kazdarkmain", "kazdarkmusicians",
         "kazdarkquestions", "kazdarksignin",
         "kazlight", "kazlightaccount", "kazlightc1", "kazlightc2", "kazlightc3",
         "kazlightc4", "kazlightc5", "kazlightc6", "kazlightcustomers", "kazlightevents",
         "kazlightg1", "kazlightg2", "kazlightg3", "kazlightg4",
         "kazlightg5", "kazlightg6", "kazlightmain", "kazlightmusicians",
         "kazlightquestions", "kazlightsignin"]

#общий маршрут
def create_route(page):
    @app.get(f"/{page}.html", response_class=HTMLResponse)
    def read_page(request: Request):
        try:   
            return templates.TemplateResponse(f"{page}.html", {"request": request})
        except Exception as e:
            print(f"Error in {page}: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

for page in pages:
    create_route(page)

# Обработчик корневого пути
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Выбираем первую страницу из списка
    page = pages[0]
    try:
        return templates.TemplateResponse(f"{page}.html", {"request": request})
    except Exception as e:
        print(f"Error in root path: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# # Маршрут регистрации
# @app.post("/register", response_class=HTMLResponse)
# async def register_user(
#     request: Request,
#     db: psycopg2.extensions.connection = Depends(get_db)
# ):
#     try:
#         form_data = await request.form()
#         user_fname = form_data.get("user_fname")
#         user_lname = form_data.get("user_lname")
#         user_email = form_data.get("user_email")
#         user_phone = form_data.get("user_phone")
#         user_password = form_data.get("user_password")
#         repeat_password = form_data.get("repeat_password")
#         agree = form_data.get("agree")

#         if user_password != repeat_password:
#             raise HTTPException(status_code=400, detail="Пароли не совпадают")

#         with db.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
#             existing_user = cursor.fetchone()
#             if existing_user:
#                 raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
#             cursor.execute(
#                 "INSERT INTO users (user_fname , user_lname , user_email , user_phone , user_password ) VALUES (%s, %s, %s, %s, %s)",
#                 (user_fname , user_lname , user_email , user_phone , user_password ),
#             )
#             db.commit()

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         print(f"Ошибка при регистрации пользователя: {e}")
#         raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
#     return templates.TemplateResponse("rusdarkmain.html", {"request": request})



# Маршрут регистрации
@app.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        form_data = await request.form()
        user_fname = form_data.get("user_fname")
        user_lname = form_data.get("user_lname")
        user_email = form_data.get("user_email")
        user_phone = form_data.get("user_phone")
        user_password = form_data.get("user_password")
        repeat_password = form_data.get("repeat_password")
        agree = form_data.get("agree")

        if user_password != repeat_password:
            raise HTTPException(status_code=400, detail="Пароли не совпадают")

        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
            existing_user = cursor.fetchone()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
            cursor.execute(
                "INSERT INTO users (user_fname , user_lname , user_email , user_phone , user_password ) VALUES (%s, %s, %s, %s, %s)",
                (user_fname , user_lname , user_email , user_phone , user_password ),
            )
            db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmain.html", {"request": request})


# Зависимость для проверки, что пользователь аутентифицирован
def get_current_user(request: Request, user_id: str = Cookie(default=None)):
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user_id

# Пример использования зависимости в вашем маршруте
@app.post("/rusdarksignin.html", response_class=HTMLResponse)
async def register_user(
    request: Request,
    db: psycopg2.extensions.connection = Depends(get_db)
    ):
    try:
        form_data = await request.form()
        user_email = form_data.get("user_email")
        user_password = form_data.get("user_password")
        # Подключение к базе данных
        conn = get_db()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Хеширование пароля (рекомендуется для безопасности)
        hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

        # Выполнение запроса для проверки имени пользователя и хешированного пароля
        cursor.execute(
            "SELECT user_id FROM users WHERE user_email = %s AND user_password = %s",
            (user_email, hashed_password),
        )

        # Получение результата запроса
        user = cursor.fetchone()

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        # Проверка результата запроса и принятие решения
        if user:
            # Успешная аутентификация
            # Перенаправление на главную страницу после входа
            return RedirectResponse(url="/rusdarkmain.html")

        else:
            # Неудачная аутентификация
            return templates.TemplateResponse(
                "rusdarksignin_failure.html", {"request": request}
            )

    except Exception as e:
        print(f"Error in rusdarksignin: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




# Маршрут добавления группы
@app.post("/add_group", response_class=HTMLResponse)
async def add_musgroup(
    request: Request,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        bandform_data = await request.form()
        band_name = bandform_data.get("band_name")
        rating = bandform_data.get("rating")
        band_specialization = bandform_data.get("band_specialization")
        band_description = bandform_data.get("band_description")
        band_experience = bandform_data.get("band_experience")
        band_location = bandform_data.get("band_location")
        band_members = bandform_data.get("band_members")
        band_roles = bandform_data.get("band_roles")
        band_contact_info = bandform_data.get("band_contact_info")
        band_average_check = bandform_data.get("band_average_check")

        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO band_details (band_name, rating, band_specialization, band_description, band_experience, band_location, band_members, band_roles, band_contact_info, band_average_check) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (band_name, rating, band_specialization, band_description, band_experience, band_location, band_members, band_roles, band_contact_info, band_average_check),
        )
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при добавлении группы: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmusicians.html", {"request": request})


# Маршрут добавления мероприятия
@app.post("/add_event", response_class=HTMLResponse)
async def add_musevent(
    request: Request,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        eventform_data = await request.form()
        event_name = eventform_data.get("event_name")
        event_specialization = eventform_data.get("event_specialization")
        event_description = eventform_data.get("event_description")
        event_experience = eventform_data.get("event_experience")
        event_location = eventform_data.get("event_location")
        event_members = eventform_data.get("event_members")
        event_roles = eventform_data.get("event_roles")
        event_contact_info = eventform_data.get("event_contact_info")

        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO event_details (event_name, event_specialization, event_description, event_experience, event_location, event_members, event_roles, event_contact_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (event_name, event_specialization, event_description, event_experience, event_location, event_members, event_roles, event_contact_info),
        )
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при добавлении группы: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmusicians.html", {"request": request})



# Маршрут удаления мероприятия
@app.delete("/drop_event", response_class=HTMLResponse)
async def drop_musevent(
    request: Request,
    event_id: int,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM event_details WHERE event_id = %s", (event_id,))
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при удалении мероприятия: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkevents.html", {"request": request})

# Маршрут удаления пользователя
@app.delete("/drop_user", response_class=HTMLResponse)
async def drop_user(
    request: Request,
    user_id: int,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmain.html", {"request": request})


# Маршрут удаления группы
@app.delete("/drop_band", response_class=HTMLResponse)
async def drop_band(
    request: Request,
    band_id: int,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM band_details WHERE band_id = %s", (band_id,))
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при удалении группы: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmusicians.html", {"request": request})


@app.put("/update_band", response_class=HTMLResponse)
async def update_band(
    request: Request,
    band_id: int,
    column: str,
    new: str,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor() as cursor:
            # Формирование SQL-запроса с проверкой на имя столбца
            sql = f"UPDATE band_details SET {column} = %s WHERE band_id = %s"
            cursor.execute(sql, (new, band_id))
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при обновлении группы: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmusicians.html", {"request": request})


# Маршрут обновления мероприятия
@app.put("/update_event", response_class=HTMLResponse)
async def update_event(
    request: Request,
    event_id: int,
    column: str,
    new: str,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor() as cursor:
            # Формирование SQL-запроса с проверкой на имя столбца
            sql = f"UPDATE event_details SET {column} = %s WHERE event_id = %s"
            cursor.execute(sql, (new, event_id))
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при обновлении группы: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkevents.html", {"request": request})


# Маршрут обновления пользователя
@app.put("/update_user", response_class=HTMLResponse)
async def update_user(
    request: Request,
    user_id: int,
    column: str,
    new: str,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        with db.cursor() as cursor:
            # Формирование SQL-запроса с проверко+й на имя столбца
            sql = f"UPDATE users SET {column} = %s WHERE user_id = %s"
            cursor.execute(sql, (new, user_id))
        db.commit()

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Ошибка при обновлении группы: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
    return templates.TemplateResponse("rusdarkmain.html", {"request": request})


# Маршрут для favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def empty_favicon():
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002, reload=True)

