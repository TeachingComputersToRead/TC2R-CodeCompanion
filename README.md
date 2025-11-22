<h1 align="center">Teaching Computers to Read:

*The Code Companion*</h1>


<p align="center">
    <img src="resources/bookcover.jpg" alt="Bookcover" width="1.75%"> <a href="https://teachingcomputers.wixsite.com/teachingcomputers">Check out the author webpage</a>
  </p>

<p align="center">
    <img src="resources/crc-mini.jpg" alt="CRC Logo" width="1.75%"> <a href="https://www.routledge.com/Teaching-Computers-to-Read-Effective-Best-Practices-in-Building-Valuab/Wagner-Kaiser/p/book/9781032484372">Check out the book on CRC Press</a>
  </p>

<p align="center">
    <img src="resources/amazon-mini.png" alt="Amazon Logo" width="1.75%"> <a href="https://www.amazon.com/dp/1032484357?ref_=cm_sw_r_ffobk_cp_ud_dp_41EW7J0HBY9A9G8A1GCP_3&bestFormat=true">Check out the book on Amazon</a>
  </p>

<br/>


<br/>

This repository contains the official code companion to the book "**Teaching Computers to Read**: Effective Best Practices in Building Valuable NLP Solutions", by [Dr. Rachel Wagner-Kaiser](https://www.linkedin.com/in/rawagnerkaiser/), with contributions from [Tim Cerino](https://www.linkedin.com/in/timcerino/).

<br/>

## Table of Contents

- [Background](#Background)<br /> 
- [Code Companion Overview](#Overview)<br />
- [Setup](#Setup)<br />
- [About the Author](#About)<br /><br />

<br />

<a name="Background"/>

## Background

Building Natural Language Processing (NLP) solutions that deliver ongoing business value is not straightforward. This book provides clarity and guidance on how to design, develop, deploy, and maintain NLP solutions that address real-world business problems.

In the book, we discuss the main challenges and pitfalls encountered when building NLP solutions. We also outline how technical choices interact with (and are impacted by) data, tools, the business goals, and integration between human experts and the AI solution. The best practices we cover here do not depend on the cutting-edge modeling algorithms or the architectural flavor of the month. We provide practical advice for NLP solutions that are adaptable to the solution’s specific technical building blocks.

Through providing best practices across the lifecycle of NLP development, this handbook will help organizations – particularly technical teams – use critical thinking to understand how, when, and why to build NLP solutions, what the common challenges are, and how to address or avoid them. By doing so, they'll deliver consistent value to their stakeholders and deliver on the promise of AI and NLP.

The **Code Companion** builds on the content covered in "Teaching Computers to Read" (TC2R) by providing a set of exercises to help readers understand the challenges, experiments, and critical thinking that are required when working through a real-life problem with real-life (messy) data.

For more general information on the book and code companion, please see the main page [here](https://github.com/TeachingComputersToRead).

<br />


<a name="Overview"/>

## Code Companion Overview


### Example Use Case

The use case presented in this repository is a common challenge of information extraction from a population of documents at scale. The goal of the business is to understand two key pieces of information - the payment terms and the limitation of liability. In order to succeed at this goal, we need to build a set of models to not only ingest and read the documents, but to identify the correct context relating to these clauses, and parse out a standardized answer.

We are presented with the following challenges:
- Data must be extracted from the source documentation
- There is a low amount of language variability in the vast majority of the documents
- Understanding the data quality, overall corpus patterns, and common language patterns of these two clauses
- Identifying a relatively small sample of data to annotate that maximizes model performance
- Building an effective and high performing approach to consistently extract
- Turning our results into a script and easily deployable solution

The code companion has two parts: a set of [Jupyter notebooks](#Notebooks), which cover the first four points above, and the [Additional Exercises](#Exercises) that cover the last point.



<a name="Notebooks"/>

### Notebooks

There are 6 main notebooks, which focus on the following topics:
1. Data Gathering and Selection2. Data Ingestion3. Pre-processing and Exploratory data analysis4. Data Understanding and Annotation5. Dataset Curation6. Modeling Approaches

In each notebook, there are a set of exercises interspersed for the developer, to facilitate and encourage hands-on interaction with the content.


<a name="Exercises"/>

### Additional Exercises

To finish the end-to-end development of this use case, there are [additional exercises](scripts/README.md) beyond the ones provided in the Jupyter notebooks. The goal of the additional exercises is to ensure that data scientists have a broader understanding of what it takes to build a fully useful solution - not a singular model.

As part of these exercises, the developer will build an end-to-end script for the ingestion of new files through to the end of creating an output that is usable and valuable for a (less technical) user.

The additional exercises are located [here](scripts/README.md) and walk the developer through key steps needed to prepare a solution for a productive, effective deployment.


<br />



<a name="Setup"/>

## Setup

### Step 1: Clone repo

The first step to getting started is to clone this repository. We recommend [this primer](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) if you are new to GitHub.

Specifically, clone via the below command for this repo:
```
git clone https://github.com/TeachingComputersToRead/TC2R-CC-UseCase1
```

<br/>

### Step 2: Set up python environment

This code companion was built in Python 3.11, with the key required packages outlined in `requirements.txt`, and the detailed versions and dependencies available in `requirements-detailed.txt`.

To install and run the provided notebooks, we strongly recommend building a virtual environment specific to this project. A setup script is provided in the repo, which can be run by: `./setup.sh` or `bash setup.sh`. Adjust permissions if necessary (`chmod +x setup.sh`).

Alternatively, ensure pyenv and virtualenv are installed locally and run each of the following lines of code from the main folder of the repo:
```
pyenv virtualenv tc2r_env
pyenv activate tc2r_env
pip install -r requirements.txt
```
<br/>

### Step 3 (Optional): Download related files

While the code companion will walk the developer through data collection, pre-processing, ingestion, and annotation (among others) steps, we have also made the primary data and data-related files available for download.

The files are available [here on HuggingFace🤗](https://huggingface.co/datasets/rwk506/TC2R-CodeCompanion-Data), and are referred to as such in the notebooks. After the developer has downloaded the `data` folder from HuggingFace🤗, this will replace the `data` folder in the repo.

While we strongly recommend the developer to go through the steps to generate the contents of the `data`, these files can be a helpful sanity check on your work.


<br/>

### Step 4: Dive into the exercises!

Get started working through the use case end-to-end! Don't forget to go beyond the notebooks with the additional exercises.


<br />



<a name="About"/>

## About the Author


Rachel Wagner-Kaiser, Ph.D., has 15 years of experience in data and AI, entering the data science field after completing her Ph.D. in astronomy. She specializes in building natural language processing solutions for real-world problems constrained by limited or messy data. Rachel leads technical teams to design, build, deploy, and maintain NLP solutions, and her expertise has helped companies organize and decode their unstructured data to solve a variety of business problems and drive value through automation.


<a href="https://www.linkedin.com/in/rawagnerkaiser">
    <img src="https://i.sstatic.net/gVE0j.png" alt="Follow me on LinkedIn!"> Connect on LinkedIn
  </a>

<br /><br />



