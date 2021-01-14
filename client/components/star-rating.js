import React from 'react'

export default function StarRating(props) {
  const rating = props.product.rating;

  return (
    <div>
      {
        <img className="star-rating" src={`/static/assets/stars/Star_rating_${rating}_of_5.png`} />
      }
    </div>
  )
}
