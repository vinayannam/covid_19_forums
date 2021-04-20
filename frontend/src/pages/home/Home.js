import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import styles from "./Home.module.css";

import FormGroup from "@material-ui/core/FormGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import FormLabel from "@material-ui/core/FormLabel";
import FormControl from "@material-ui/core/FormControl";

import Post from "./../../components/post";

import Accordion from "@material-ui/core/Accordion";
import AccordionSummary from "@material-ui/core/AccordionSummary";
import AccordionDetails from "@material-ui/core/AccordionDetails";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

import searchImage from "./../../assets/search.svg";

function Home() {
  const [posts, setPosts] = useState([]);
  const [filterList, setFilterList] = useState([]);
  const [filters, setFilters] = useState({});
  const [authorsList, setAuthorsList] = useState([]);
  const [topKeywordsList, setTopKeywordsList] = useState([]);
  // const [searchInput, setSearchInput] = useState("{}");

  const [_bodyParts, setBodyParts] = useState([]);
  const [_drugs, setDrugs] = useState([]);
  const [_symptoms, setSymptoms] = useState([]);
  const [_treatments, setTreatments] = useState([]);

  const searchInputRef = useRef();

  const handleChange = (label) => {
    const dup = { ...filters };
    dup[label] = !dup[label];
    setFilters(dup);
  };

  const handleFilters = (_filters) => {
    const filterObj = {};
    for (let eachSection of _filters) {
      for (let eachFilter of eachSection.filterItems) {
        filterObj[eachFilter] = false;
      }
    }
    setFilters(filterObj);
    setFilterList(_filters);
  };

  const handlePosts = (_posts) => {
    let newPosts = [..._posts];

    newPosts = newPosts.map((post) => {
      post["showAll"] = false;

      let empt = [];
      empt.push(...post.bodyparts);
      empt.push(...post.drugs);
      empt.push(...post.symptoms);
      empt.push(...post.treatments);
      post.keywordsFull = [...empt];
      post.keywords = empt.splice(0, 10);

      if (localStorage.getItem(post.title)) {
        console.log("yes");
        post["liked"] = JSON.parse(localStorage[post.title]);
      } else {
        post["liked"] = false;
      }
      return post;
    });
    sortPosts(newPosts);
    setPosts(sortPosts(newPosts));
  };

  const sortPosts = (posts_) => {
    // posts_.sort(function (x, y) {
    //   // true values first
    //   return x.liked === y.liked ? 0 : x ? -1 : 1;
    //   // false values first
    //   // return (x === y)? 0 : x? 1 : -1;
    // });
    // console.log("sorted", posts_);
    let newPosts = [];
    let authors = [];
    if (localStorage.getItem("authors")) {
      authors = new Set(JSON.parse(localStorage.getItem("authors")));
    } else {
      authors = new Set([]);
    }
    setAuthorsList([...authors]);

    posts_.forEach((post) => {
      if (authors.has(post.author)) {
        newPosts.splice(0, 0, post);
      } else {
        newPosts.push(post);
      }
    });

    return newPosts;
  };
  const setKeywords = (bd, dr, sy, tr) => {
    setBodyParts(bd);
    setDrugs(dr);
    setSymptoms(sy);
    setTreatments(tr);
  };

  const updatePosts = (title, bool, authors) => {
    const newPosts = [...posts];
    for (let each of newPosts) {
      if (each.title === title) {
        each.liked = bool;
      }
    }

    let localAuthors = [];
    if (localStorage.getItem("authors")) {
      localAuthors = new Set(JSON.parse(localStorage.getItem("authors")));
    } else {
      localAuthors = new Set([]);
    }
    setPosts([...newPosts]);

    setAuthorsList([...localAuthors]);
  };

  const getData = useCallback(() => {
    const url = "http://localhost:5001/home";
    const static_url = "https://api.jsonbin.io/b/607f22bb45d8dc07adb51495";

    let searchTerm = "covid";
    if (searchInputRef.current.value) {
      searchTerm = searchInputRef.current.value;
    }
    console.log("search");
    // axios.post(url, { "search": searchTerm }).then((res) => {
    axios.get(static_url).then((res) => {
      handlePosts(res.data.posts);
      const localObj = res.data.keyword;
      setKeywords(
        localObj.bodyparts,
        localObj.drugs,
        localObj.symptoms,
        localObj.treatments
      );
      setTopKeywordsList(res.data.top_keyword);

      // handleFilters(res.data.filters);
    });
  }, []);

  useEffect(() => {
    getData();
  }, [getData]);

  const search = () => {
    getData();
  };

  const visitLink = (text) => {
    if (text == "covid") {
      window.open(
        "https://www.worldometers.info/coronavirus/country/us/",
        "_blank"
      );
    } else {
      window.open(
        "https://azdhs.gov/covid19/vaccines/index.php#registration",
        "_blank"
      );
    }
  };

  return (
    <div>
      <header className={styles.header}>
        Semantic Web Mining - Healthcare Mining
        <div className={styles.headerBtns}>
          <div
            onClick={() => visitLink("covid")}
            className={styles.headerLinks}
          >
            Covid Cases
          </div>
          <div
            onClick={() => visitLink("vaccine")}
            className={styles.headerLinks}
          >
            Vaccination
          </div>
        </div>
      </header>

      <div className={styles.pageBody}>
        <div className={styles.splitScreen}>
          <div className={styles.sidebar}>
            {/* Authors list */}
            {authorsList.length > 0 && (
              <div className={styles.authorListWrap}>
                <div className={styles.authorsListTitle}>
                  Following authors:
                </div>

                {authorsList.map((author) => (
                  <div key={author} className={styles.eachAuthor}>
                    {author}
                  </div>
                ))}
              </div>
            )}

            {/* Top keywords */}
            {topKeywordsList.length > 0 && (
              <div className={styles.authorListWrap}>
                <div className={styles.authorsListTitle}>Top Keywords:</div>

                {topKeywordsList.map((author) => (
                  <div key={author} className={styles.eachAuthor}>
                    {author}
                  </div>
                ))}
              </div>
            )}

            <div>
              {/* bodyparts */}
              {_bodyParts.length > 0 && (
                // <div className={styles.eachSidebarSection}>
                <Accordion>
                  {_bodyParts.length > 0 && (
                    // <div className={styles.eachSidebarSectionHeader}>
                    <AccordionSummary
                      className={styles.eachSidebarSectionHeader}
                      expandIcon={<ExpandMoreIcon />}
                      aria-controls="panel1a-content"
                      id="panel1a-header"
                    >
                      Body Parts keywords:
                    </AccordionSummary>
                    // {/* </div> */}
                  )}

                  <AccordionDetails>
                    <div>
                      {_bodyParts.length > 0 &&
                        _bodyParts.map((keyW, index) => (
                          <div
                            key={index}
                            className={styles.eachSidebarSymptomItem}
                          >
                            {keyW}
                          </div>
                        ))}
                    </div>
                  </AccordionDetails>
                </Accordion>
                // {/* </div> */}
              )}
              {/* drugs */}
              {_drugs.length > 0 && (
                // <div className={styles.eachSidebarSection}>
                <Accordion>
                  {_drugs.length > 0 && (
                    // <div className={styles.eachSidebarSectionHeader}>
                    <AccordionSummary
                      className={styles.eachSidebarSectionHeader}
                      expandIcon={<ExpandMoreIcon />}
                      aria-controls="panel1a-content"
                      id="panel1a-header"
                    >
                      Drugs keywords:
                    </AccordionSummary>
                    // {/* </div> */}
                  )}

                  <AccordionDetails>
                    <div>
                      {_drugs.length > 0 &&
                        _drugs.map((keyW, index) => (
                          <div
                            key={index}
                            className={styles.eachSidebarSymptomItem}
                          >
                            {keyW}
                          </div>
                        ))}
                    </div>
                  </AccordionDetails>
                </Accordion>
                // {/* </div> */}
              )}
              {/* symptoms */}
              {_symptoms.length > 0 && (
                // <div className={styles.eachSidebarSection}>
                <Accordion>
                  {_symptoms.length > 0 && (
                    // <div className={styles.eachSidebarSectionHeader}>
                    <AccordionSummary
                      className={styles.eachSidebarSectionHeader}
                      expandIcon={<ExpandMoreIcon />}
                      aria-controls="panel1a-content"
                      id="panel1a-header"
                    >
                      Symptoms keywords:
                    </AccordionSummary>
                    // {/* </div> */}
                  )}

                  <AccordionDetails>
                    <div>
                      {_symptoms.length > 0 &&
                        _symptoms.map((keyW, index) => (
                          <div
                            key={index}
                            className={styles.eachSidebarSymptomItem}
                          >
                            {keyW}
                          </div>
                        ))}
                    </div>
                  </AccordionDetails>
                </Accordion>
                // {/* </div> */}
              )}
              {/* treatments */}
              {_treatments.length > 0 && (
                // <div className={styles.eachSidebarSection}>
                <Accordion>
                  {_treatments.length > 0 && (
                    // <div className={styles.eachSidebarSectionHeader}>
                    <AccordionSummary
                      className={styles.eachSidebarSectionHeader}
                      expandIcon={<ExpandMoreIcon />}
                      aria-controls="panel1a-content"
                      id="panel1a-header"
                    >
                      Treatments keywords:
                    </AccordionSummary>
                    // {/* </div> */}
                  )}

                  <AccordionDetails>
                    <div>
                      {_treatments.length > 0 &&
                        _treatments.map((keyW, index) => (
                          <div
                            key={index}
                            className={styles.eachSidebarSymptomItem}
                          >
                            {keyW}
                          </div>
                        ))}
                    </div>
                  </AccordionDetails>
                </Accordion>
                // {/* </div> */}
              )}
            </div>
          </div>

          <div className={styles.articles}>
            <div className={styles.inputBarWrap}>
              <div className={styles.inputBarRow}>
                <div className={styles.inputbar}>
                  <input
                    className={styles.inputSearch}
                    ref={searchInputRef}
                    type="text"
                    placeholder="Search COVID-19 related topics"
                  ></input>
                  <div className={styles.inputSearchBtn} onClick={search}>
                    <img alt="search" height="30" src={searchImage}></img>
                  </div>
                </div>
                <div className={styles.topbtnrow}>
                  <button
                    onClick={() => visitLink("covid")}
                    className={styles.btnSecondaryTop}
                  >
                    Covid Cases
                  </button>
                  <button
                    onClick={() => visitLink("vaccine")}
                    className={styles.btnSecondaryTop}
                  >
                    Vaccination
                  </button>
                </div>
              </div>
            </div>

            <div className={styles.postsWrapper}>
              {posts.map((post, index) => (
                <Post
                  onLike={updatePosts}
                  key={index}
                  post={post}
                  index={index}
                  showAll={false}
                ></Post>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
