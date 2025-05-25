import psycopg2
from psycopg2 import sql

class DatabaseManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)
        self.conn.autocommit = True

    def add_pass(self, pass_data):
        try:
            with self.conn.cursor() as cursor:
                # Проверка обязательных полей
                required_fields = ['beauty_title', 'title', 'user', 'coords', 'level']
                for field in required_fields:
                    if field not in pass_data:
                        return {'status': 400, 'message': f'Missing required field: {field}', 'id': None}

                # Добавление/обновление пользователя
                user = pass_data['user']
                cursor.execute(
                    """
                    INSERT INTO users (email, fam, name, otc, phone)
                    VALUES (%(email)s, %(fam)s, %(name)s, %(otc)s, %(phone)s)
                    ON CONFLICT (email) DO UPDATE
                    SET fam = EXCLUDED.fam, name = EXCLUDED.name, otc = EXCLUDED.otc, phone = EXCLUDED.phone
                    RETURNING id
                    """,
                    user
                )
                user_id = cursor.fetchone()[0]

                # Добавление перевала
                coords = pass_data['coords']
                level = pass_data['level']
                cursor.execute(
                    """
                    INSERT INTO passes (
                        beauty_title, title, other_titles, connect, add_time, user_id,
                        latitude, longitude, height, winter, summer, autumn, spring
                    )
                    VALUES (%(beauty_title)s, %(title)s, %(other_titles)s, %(connect)s, 
                            %(add_time)s, %(user_id)s, %(latitude)s, %(longitude)s, 
                            %(height)s, %(winter)s, %(summer)s, %(autumn)s, %(spring)s)
                    RETURNING id
                    """,
                    {
                        **pass_data,
                        'user_id': user_id,
                        'latitude': coords['latitude'],
                        'longitude': coords['longitude'],
                        'height': coords['height'],
                        'winter': level.get('winter'),
                        'summer': level.get('summer'),
                        'autumn': level.get('autumn'),
                        'spring': level.get('spring'),
                        'add_time': pass_data.get('add_time')
                    }
                )
                pass_id = cursor.fetchone()[0]

                # Добавление изображений
                if 'images' in pass_data:
                    for image in pass_data['images']:
                        cursor.execute(
                            "INSERT INTO images (pass_id, data, title) VALUES (%s, %s, %s)",
                            (pass_id, image['data'], image['title'])
                        )

                return {'status': 200, 'message': 'Success', 'id': pass_id}

        except Exception as e:
            return {'status': 500, 'message': f'Database error: {str(e)}', 'id': None}

    def close(self):
        self.conn.close()