# PageRank Algorithm-Based Movie Recommendation System

## 1. Introduction

The **PageRank algorithm** is a widely used technique for ranking nodes in a graph based on their relative importance. Originally developed by Larry Page and Sergey Brin for search engines, it also finds applications in recommendation systems. This project explores how PageRank, combined with the **Power Method** and **Limiting Probability**, can be applied to a **Movie Recommendation System**.

---

## 2. PageRank Algorithm

### 2.1 Definition and Concept

PageRank assigns a numerical value to each node (e.g., a movie) in a graph, reflecting its importance based on connections to other nodes. A node becomes more important if it's linked to by other important nodes.

### 2.2 Mathematical Formulation

The PageRank score of a node \( P \) is given by:

\[
PR(P) = \frac{1 - d}{N} + d \cdot \sum \frac{PR(P_i)}{L(P_i)}
\]

Where:
- \( PR(P) \) = PageRank of node \( P \)  
- \( d \) = Damping factor (typically 0.85)  
- \( N \) = Total number of nodes  
- \( P_i \) = Nodes linking to \( P \)  
- \( L(P_i) \) = Number of outgoing links from \( P_i \)

### 2.3 Computation using the Power Method

An iterative approach used to compute the dominant eigenvector of a matrix (i.e., steady-state probability distribution).

**Steps:**
1. Initialize PageRank vector with equal values.
2. Iteratively multiply by transition matrix:  
   \[
   PR^{(new)} = M \cdot PR^{(old)}
   \]
3. Repeat until convergence (i.e., change between iterations is below a threshold).

### 2.4 Limiting Probability

In Markov Chains, the **Limiting Probability** represents the steady-state distribution. The Power Method drives PageRank to this steady state, yielding stable importance scores for each movie.

---

## 3. Project Idea: Movie Recommendation System

### 3.1 Problem Statement

Traditional recommendation systems (collaborative or content-based) often ignore deeper interconnections between items. PageRank allows us to model **movie similarity as a graph**, ranking movies by importance in that network.

### 3.2 Graph Representation

- **Nodes**: Movies  
- **Edges**: Similarities between movies (genre, storyline)  
- **Edge Weights**: Cosine similarity + user ratings

### 3.3 Application of PageRank

1. Construct a movie similarity graph.
2. Build the transition probability matrix.
3. Apply PageRank via Power Iteration.
4. Recommend top-scoring movies.

### 3.4 Advantages

- Captures indirect (multi-hop) relationships.
- Mitigates cold-start problems.
- Scalable to large movie datasets.

---

## 4. Implementation Overview

### 4.1 Data Collection

- Used curated dataset with:
  - Titles, genres, plot summaries, optional user ratings
- Applied **TF-IDF vectorization** on plot summaries
- Computed **cosine similarity** between movie vectors

### 4.2 Algorithm Execution

- **Graph Construction**:
  - Each movie is a node
  - Edges based on cosine similarity and optional rating weight

- **Transition Matrix**:
  - Built a stochastic matrix using normalized edge weights
  - Combined textual and rating similarities

- **PageRank Computation**:
  - Used Power Method to compute final importance scores

- **Recommendation Ranking**:
  - Sorted nodes by PageRank score
  - Returned top-ranked neighbors for recommendations

### 4.3 Evaluation

- Compared with standard collaborative filtering models  
- Evaluated using:
  - Ranking consistency
  - User satisfaction (survey/test user feedback) — optional

---

## 5. Demo

_(Demo is in PageRank_Movie_Recommendation.file)_

---

## 6. Conclusion

By applying **PageRank**, **Power Iteration**, and **Limiting Probability**, this project demonstrates a scalable and effective approach to movie recommendations. This graph-based method leverages inter-movie relationships more robustly than traditional techniques and offers a novel way to enhance personalization in recommendation systems.
