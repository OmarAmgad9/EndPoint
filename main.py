import contextlib
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client['courses']


# this endpoint allows your retrieve alist of all availble courses , you can sort the courses based on different criteria
@app.get('/courses')
def get_courses(sort_by: str = 'date', domain: str = None):
    # Set the rating.total and rating.count to all the courses based on the sum of chapters rating
    for course in db.courses.find():
        total = 0
        count = 0
        for chapter in course['chapters']:
            with contextlib.suppress(KeyError):
                total += chapter['rating']['total']
                count += chapter['rating']['count']
    
    # sort_by == date [DESCENAING]
    if sort_by == 'date':
        sort_filed = 'date'
        sort_order = -1
    
    elif sort_by == 'rating':
        sort_filed = 'rating.total'
        sort_order = -1

    else:
        sort_filed = 'name'
        sort_order = 1
    query = {}
    if domain:
        query['domain'] = domain
    
    courses = db.courses.find(query, {'name': 1, 'date': 1, 'description': 1, 'domain': 1, 'rating': 1, '_id': 0 }).sort(sort_filed, sort_order)

    return list(courses)

@app.get('/courses/{course_id}')
def get_course(course_id: str):
    course = db.coureses.find_one({'_id': ObjectId(course_id)}, {'_id': 0, 'chapters': 0})
    if not course:
        raise HTTPException(status_code=404, detail='Course Not Found')
    try: 
        course['rating'] = course['rating']['total']
    except KeyError:
        course['rating'] = 'Not Rated Yet'
    return course

@app.get('/courses/{course_id}/{chapter_id}')
def get_chapter(course_id: str, chapter_id: str):
    course = db.courses.find_one({'_id': ObjectId(course_id)}, {'_id':0})
    if not course:
        raise HTTPException(status_code=404, detial='Course Not Found')
    chapters = course.get('chapters', [])
    try:
        chapter = chapters[int(chapter_id)]
    except (ValueError, IndexError) as e:
        raise HTTPException(status_code=404, detail='Chapter not found') from e
    return chapter