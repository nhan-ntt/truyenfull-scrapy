from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from core.models import Story, Chapter, Genre
from core.schemas import StorySchema, ChapterSchema, GenreSchema
from adapters.PostgresGenreRepository import PostgresGenreRepository
from adapters.PostgresStoryRepository import PostgresStoryRepository
from adapters.PostgresChapterRepository import PostgresChapterRepository

from core.models import Base

DATABASE_URL = "postgresql://postgres:thanhnhan1911@localhost:5432/nhon"
# DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
# hehe
Sessionlocal = sessionmaker(bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Dependency to get the genre repository
def get_genre_repository(db: Session = Depends(get_db)):
    return PostgresGenreRepository(db)


# Dependency to get the story repository
def get_story_repository(db: Session = Depends(get_db)):
    return PostgresStoryRepository(db)


# Dependency to get the chapter repository
def get_chapter_repository(db: Session = Depends(get_db)):
    return PostgresChapterRepository(db)


# API Routes for genre
@app.get("/genres/{genre_id}", response_model=None)
def read_genre(
        genre_id: int,
        genre_repo: PostgresGenreRepository = Depends(get_genre_repository)
):
    return genre_repo.get_genre(genre_id)


@app.get("/search/{keyword}", response_model=None)  # search
def search_story(
        keyword: str,
        story_repo: PostgresStoryRepository = Depends(get_story_repository)
):
    return story_repo.search(keyword)


@app.get("/genres/", response_model=None)
def read_all_genres(genre_repo: PostgresGenreRepository = Depends(get_genre_repository)):
    return genre_repo.get_all_genres()


# API routes for Story
@app.post("/stories/", response_model=dict)
def create_story(
        story: StorySchema,
        story_repo: PostgresStoryRepository = Depends(get_story_repository)
):
    return story_repo.create_story(
        genre_id=story.genre_id,
        title=story.title,
        description=story.description,
        author=story.author
    )


@app.get("/stories/{story_id}", response_model=None)
def read_story(
        story_id: int,
        story_repo: PostgresStoryRepository = Depends(get_story_repository)
):
    return story_repo.read_story_by_id(story_id)


@app.get("/stories/genre/{genre_id}", response_model=None)
def read_all_stories_of_genre(
        genre_id: int,
        story_repo: PostgresStoryRepository = Depends(get_story_repository)
):
    return story_repo.read_stories_of_genre(genre_id)


@app.put("/stories/{story_id}", response_model=None)
def update_story(
        story_id: int,
        updated_story: StorySchema,
        story_repo: PostgresStoryRepository = Depends(get_story_repository)
):
    return story_repo.update_story(story_id, updated_story)


@app.delete("/stories/{story_id}")
def delete_story(
        story_id: int,
        story_repo: PostgresStoryRepository = Depends(get_story_repository)
):
    story_repo.delete_story(story_id)
    return {"message": "Story deleted successfully"}


# API routes for Chapter
@app.post("/chapters/", response_model=None)
def create_chapter(
        chapter: ChapterSchema,
        chapter_repo: PostgresChapterRepository = Depends(get_chapter_repository)
):
    return chapter_repo.create_chapter(
        story_id=chapter.story_id,
        title=chapter.title,
        content=chapter.content
    )


@app.get("/chapters/story/{story_id}/chapter/{chapter_id}", response_model=None)
def read_chapter(
        story_id: int,
        chapter_id: int,
        chapter_repo: PostgresChapterRepository = Depends(get_chapter_repository)
):
    return chapter_repo.read_chapter_by_id(story_id, chapter_id)


@app.get("/chapters/story/{story_id}", response_model=None)
def read_chapters_of_a_story(
        story_id: int,
        chapter_repo: PostgresChapterRepository = Depends(get_chapter_repository)
):
    return chapter_repo.read_chapters_of_story(story_id)

# @app.put("/chapters/{chapter_id}", response_model=None)
# def update_chapter(chapter_id: int, updated_chapter: Chapter, chapter_repo: PostgresChapterRepository = Depends(get_chapter_repository)):
#     return chapter_repo.update_chapter(updated_chapter)

# @app.delete("/chapters/{chapter_id}")
# def delete_chapter(chapter_id: int, chapter_repo: PostgresChapterRepository = Depends(get_chapter_repository)):
#     chapter_repo.delete_chapter(chapter_id)
#     return {"message": "Chapter deleted successfully"}
