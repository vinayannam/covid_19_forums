import styles from "./Post.module.css";
import React, { useState, useEffect } from "react";
import commentImage from "./../../assets/comment.svg";
import visitImage from "./../../assets/forward.svg";
import likeImageFilled from "./../../assets/like-filled.svg";
import likeImage from "./../../assets/like.svg";
import userImage from "./../../assets/user.svg";

function Post({ index, post, showAll, onLike }) {
  const [showAllState, setShowAllState] = useState(showAll);
  const [isLiked, setIsLiked] = useState(post.liked);
  useEffect(() => {
    // getData();
  }, []);

  const showMore = () => {
    setShowAllState(true);
  };

  const showLess = () => {
    setShowAllState(false);
  };

  const likePost = () => {
    let temp = isLiked;
    temp = !temp;
    if (temp) {
      let authors = JSON.parse(localStorage.getItem("authors"));
      let authors_set = new Set(authors);
      if (authors === null) {
        authors = [];
      }
      if (!authors_set.has(post.author)) {
        authors.push(post.author);
      }
      localStorage.setItem("authors", JSON.stringify(authors));
      localStorage.setItem(post.title, temp);
      onLike(post.title, temp, authors);
    } else {
      let authors = JSON.parse(localStorage.getItem("authors"));
      const index = authors.indexOf(post.author);
      if (index > -1) {
        authors.splice(index, 1);
      }
      localStorage.setItem("authors", JSON.stringify(authors));
      localStorage.removeItem(post.title);
      onLike(post.title, temp, authors);
    }

    setIsLiked(temp);
  };

  return (
    <div>
      <div key={index} className={styles.eachArticle}>
        <div className={styles.eachArticleTitle}>
          <div>{post.title}</div>
          <div className={styles.eachArticleAuthor}>
            <img src={userImage} alt="" height="17"></img>
            <div>{post.author}</div>
          </div>
        </div>
        <div className={styles.eachArticleDescription}>{post.content}</div>

        {!showAllState && post.keywords.length > 0 && (
          <div className={styles.eachArticleKeywords}>
            {post.keywords.map((keyword, index) => (
              <div key={index} className={styles.eachKeyword}>
                {keyword}
              </div>
            ))}
            <div className={styles.showButton} onClick={() => showMore()}>
              Show more...
            </div>
          </div>
        )}

        {showAllState && post.keywordsFull.length > 0 && (
          <div className={styles.eachArticleKeywords}>
            {post.keywordsFull.map((keyword, index) => (
              <div key={index} className={styles.eachKeyword}>
                {keyword}
              </div>
            ))}
            <div className={styles.showButton} onClick={() => showLess()}>
              Show less
            </div>
          </div>
        )}

        <div className={styles.postLastRow}>
          <div className={styles.flex}>
            <div onClick={likePost} className={styles.repliesItemLike}>
              {!isLiked && (
                <img
                  alt=""
                  height="25"
                  className={styles.repliesItemLikeImg}
                  src={likeImage}
                ></img>
              )}

              {isLiked && (
                <img
                  alt=""
                  height="25"
                  className={styles.repliesItemLikeImg}
                  src={likeImageFilled}
                ></img>
              )}

              {!isLiked && <div>Like</div>}
              {isLiked && <div>Unlike</div>}
            </div>
            <div className={styles.repliesItem}>
              <img alt="" height="25" src={commentImage}></img>
              <div>{post.replies}</div>
            </div>
          </div>
          <div className={styles.repliesItem}>
            {/* <button className={styles.btnSecondary}>Visit Website</button> */}
          </div>
          <a
            className={styles.repliesItem}
            target="_blank"
            href={post.url}
            rel="noreferrer"
          >
            <div>Go to Post</div>
            <img
              alt=""
              className={styles.visitImage}
              height="25"
              src={visitImage}
            ></img>
          </a>
        </div>
      </div>
    </div>
  );
}

export default Post;
