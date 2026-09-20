
from fastapi import APIRouter, Query, HTTPException
from fastapi import Depends
from sqlmodel import Session, select,func
from database import get_session
from models import Review, ReviewRead, ReviewCreate, ReviewUpdate

router= APIRouter(prefix="/reviews", tags=["reviews"])
# this /  below means  /reviews/
#  session part is the dependency injection
@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session:Session= Depends (get_session)):
    db_review= Review(**review.model_dump()) # this is the unpacking dictionary.model dump converts the pydentic object into dictionary
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review




@router.get("/", response_model=list[ReviewRead])
def list_reviews(play_name:str | None=Query(None, description="Filter by play name"),
                 skip:int=Query(0,ge=0, description="Number of reviews to skip"),
                 limit:int=Query(10,ge=1,le=50, description="Maximum number of reviews to return"),
                 session:Session=Depends(get_session)
                 ):
    query=select(Review) # i select a review

    if play_name:
        query=query.where(Review.play_name==play_name)
    query=query.offset(skip).limit(limit)
    reviews=session.exec(query).all()
    return reviews


@router.get("/average/{play_name}")
def get_average_rating(play_name:str, session:Session=Depends(get_session)):
    result=session.exec(
        select(func.avg(Review.rating),func.count(Review.id)).where(Review.play_name==play_name)
    ).first()
    avg_rating, total= result
    if total==0:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"play_name":play_name,"avg_rating":round(avg_rating,2),"total_reviews":total}


@router.get("/{review_id}",response_model=ReviewRead)
def get_review(review_id: int, session:Session=Depends(get_session)):
    review=session.get(Review,review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.patch("/{review_id}",response_model=ReviewRead)
def update_review(review_id: int,update:ReviewUpdate, session:Session=Depends(get_session)):
    review=session.get(Review,review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    updated_data=update.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(review,key,value)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

@router.delete("/{review_id}")
def delete_review(review_id: int, session:Session=Depends(get_session)):
    review=session.get(Review,review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"message":"Review deleted"}
