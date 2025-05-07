# ReSearchy: Guarding Novelty, Guiding Ideas

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ReSearchy is a platform and planned plugin tool designed to assist researchers in the early stages of ideation by identifying potential overlaps with existing academic literature. Our goal is to help prevent redundant work and guide researchers towards more novel and impactful contributions.

## 🧑‍💻 Team Members

* **Ya-Ting Pai** (yatingp2@illinois.edu)
* **Shilong Li** (sli148@illinois.edu)
* **Yixuan Li** (yixuan19@illinois.edu)
* **Xuanming Zhang** (xz130@illinois.edu)

This project was developed as part of the CS510 Advanced Information Retrieval course at the University of Illinois Urbana-Champaign.

## 📖 About The Project

One of the most significant challenges in academic research is investing substantial time and effort into an idea, only to discover later that similar work has already been published. ReSearchy aims to mitigate this by providing an early warning system. By leveraging semantic matching, it helps researchers quickly understand how their ideas relate to the current body of knowledge, overcoming limitations of traditional literature review methods that can miss conceptually similar work due to differences in terminology.

With ReSearchy, the research process becomes more efficient, allowing academic resources to be focused on genuine knowledge gaps rather than reinventing existing work.

## 🚀 How It Works

1.  **User Input:** A researcher inputs their research idea or abstract into the ReSearchy platform.
2.  **Semantic Processing:** The input text is processed by a pre-trained language model to generate a semantic representation.
3.  **Database Search:** This embedding is used to query an indexed database of existing research paper embeddings using efficient retrieval methods.
4.  **Similarity Ranking:** The system retrieves the most semantically similar papers.
5.  **Overlap Analysis & Display:**
    * Titles and abstracts of potentially overlapping papers are presented to the user.
    * For selected papers, with NLP techniques used to highlight specific sentences or phrases that are conceptually similar to the user's input.

## 🏁 Getting Started

### Prerequisites

* Python 3.x
* Node.js & npm/yarn (for frontend)
* Milvus and stored embeddings

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/averypai/ReSearchy.git
    ```
2.  Install backend dependencies
    ```sh
    cd ReSearchy/backend
    pip install -r requirements.txt
    ```
3.  Install frontend dependencies
    ```sh
    cd ../frontend
    npm install
    ```
4.  Set up environment variables for Milvus on the Cloud

### Running the Application

1.  Start the backend server:
    ```sh
    # From the backend directory
    python -m uvicorn main:app --reload
    ```
2.  Start the frontend development server:
    ```sh
    # From the frontend directory
    npm start
    ```
3.  Open your browser and navigate to `http://localhost:8000` (or the port your frontend runs on).


## 🛠️ Tech Stack

* **Backend:** Python
* **Frontend:** Javascript
* **Semantic Retrieval:** Milvus
* **Initial Data Source:** arXiv API
* **NLP/Semantic Matching**


## 🛣️ Future Work

* **Plugin Integration:** Develop a Chrome extension or plugins for popular writing platforms (e.g., Overleaf, MS Word) for seamless integration into researchers' workflows.
* **Expanded Data Sources:** Incorporate more academic databases beyond arXiv.
* **User Accounts & History:** Allow users to save searches and track their idea evolution.
* **Advanced Filtering:** Provide more sophisticated filtering options for search results.
* **Collaborative Features:** Enable teams to work together on idea validation.

## 📜 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## 🙏 Acknowledgements

* The arXiv team for their API and open-access dataset.
* Professor Chengxiang Zhai and the CS510 course staff.

---
**Project Link:** [https://github.com/averypai/ReSearchy](https://github.com/averypai/ReSearchy)
