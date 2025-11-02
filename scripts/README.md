<h1 align="center">Additional Exercises:

*For a Useful End-to-End Solution*</h1>

## Table of Contents

- [Background](#Background)
- [1. End-to-End Script](#end2end)
- [2. Unit Tests](#UnitTest)
- [3. Logging](#Logging)
- [4. Output Options](#Output)
- [5. Model Card](#ModelCard)
- [6. Input Options](#InputOptions)
- [7. Containerize](#Containerize)
- [Conclusion](#Conclusion)
- [About the Author](#About)

<br />

<a name="Background"/>

## Background

To finish the end-to-end development of the information extraction use case (outlined [here](../README.md)), there are [additional exercises](scripts/README.md) beyond the ones provided in the Jupyter notebooks. The goal of the additional exercises is to ensure that data scientists have a broader understanding of what it takes to build a fully useful solution - not a singular model.

As part of these exercises, the developer will finish an end-to-end script for the ingestion of new files through to the end of creating an output that is usable and valuable for a (less technical) user.

The additional exercises below walk the developer through key steps (at a high level) needed to prepare a solution for a productive, effective deployment.

**Two notes here for the developer**, before getting started on these exercises:
- As the developer progresses through the additional exercises below, you may note that these steps take as much or more time than the original development process. This is representative of the breakdown of efforts - it often takes many times more effort to deploy a production-level solution that it does to build the underlying AI pieces. 
- We encourage the use of LLMs and similar tools as co-code developers in this section. However, as usual, heed the typical warnings: provide detailed instructions, specific inputs and outputs, review the generated code, and test thoroughly to ensure it aligns with the behavior desired by you as a developer.



<br/>

<a name="end2end"/>

## 1. End-to-End Script

Let's start by piecing together what we built in the notebook development and exercises into a cohesive script.

We have started this process for the developer, and the exercises below expand on the initial work to add in additional capabilities (e.g. date parser to an integer) into our end-to-end pipeline and final output.


### **Exercise 1.1**

Review the existing main end-to-end script:
- Inside the `scripts` folder, you will find the `pipeline.py` script and the corresponding `helper_functions.py` scripts contain the main functions for end-to-end behavior (these functions should be very familiar from the notebooks!).
- Confirm your understanding of each of the main functions' inputs, outputs, and data types.
- Test the `pipeline.py` file by running it on a folder containing a handful of documents, and confirm the output excel spreadsheet contains the relevant information


### **Exercise 1.2**

Create an additional function in the `helper_function.py` file to add a "day parser" function. This function should leverage the extracted context (input) to parse out the number of days from the context as an integer (output).


### **Exercise 1.3**

Add the "day parser" function into the end-to-end `pipeline.py` script, to ensure the function is run as an additional step whenever


### **Exercise 1.4**

As the days are now being parsed out of the context as integers, add this information for each document as an additional column in the output excel file for the (less technical) users.



### **Exercise 1.5**

Test the functionality and confirm the output. This can be done with a subset (50-100) files, if needed (rather than the entire corpus).



<br/>

<a name="UnitTest"/>

## 2. Unit Tests

In standard software engineering practices, the unit tests are often written first and used as a gauge of progress and success as code is developed ("test driven development").

However, things can get tricky when we don't always know what the solution is going to look like ahead of time with AI and NLP projects. Uncertainty arises from a variety of places - probabilistic outputs, uncertainty about which models will perform sufficiently, uncertainty in where performance will land, incomplete knowledge of the corpus and edge cases, and so on. In this case, we haven't built out our unit tests ahead of time (partly due to these uncertainties and partly due to the structure of the code companion). 

Now, let's continue the development of the unit tests. We'll focus primarily on functionality - data/input/output types and validation, pipeline integrity, error handling, edge cases, etc.

In addition to the unit tests below, note that adjustments may be needed for original functions if certain functionality is missing!


### **Exercise 2.1**

Review the existing unit tests provided:
- In the `scripts` folder, the `unit_tests.py` script and the corresponding `tests` folder contain initial unit tests written for three functions:
	- `pdf_to_text_with_ocr` (see `TestPdfToTextWithOcr` class in `unit_tests.py`)
	- `pull_text_from_html` (see `TestPullTextFromHtml` class in `unit_tests.py`)
	- `read_text_files` (see `TestReadTextFiles` class in `unit_tests.py`)
- Confirm your understanding of each test case's inputs, outputs, and goal.
- Confirm the behavior of the unit tests by running it - it will run leveraging the example documents in the `tests/docs` folder.


### **Exercise 2.2**

For the other key helper functions, add similar unit tests to the test suite:
- `calculate_ocr_quality`
- `plot_ocr_quality_histogram`
- `process_texts_to_dataframe`
- `run_classification_model`



### **Exercise 2.3**

What other scenarios should be tested across our functions? Identify at least 3 more cases and add those scenarios to the unit tests.



### **Exercise 2.4**

Create additional unit tests for the full end-to-end pipeline as well in `pipeline.py`, specifically the `process_and_classify_files` function.




### **Exercise 2.5**

Run the full test suite and confirm all tests pass. What is the overall line and function coverage of the test suite?

(For those new to unit tests and coverage, see this [great article](https://www.atlassian.com/continuous-delivery/software-testing/code-coverage) by Atlassian).



<br/>

<a name="Logging"/>

## 3. Logging

Most of us have been there at some point - something is failing and it is failing silently. It creates a headache.

Logging is critical to help mitigate (if not avoid) such headaches by providing some level of transparency into how our solution is progressing, processing, and calling functions. Because there can be so many inter-dependent steps in NLP and AI solutions, it's helpful to have visibility at each step in our pipeline.

The code has started with some existing, basic logging already - in this section we'll expand on it.


### **Exercise 3.1**

Review the logging already present in `pipeline.py` to familiarize yourself with the existing logging.

Review the output logs as well, which were generated during Exercise 1.5, to see what the output structure looks like.



### **Exercise 3.2**

Add additional informational logging that identifies the number of files identified and being processed in the `process_and_classify_files` function. Consider providing counts by file type and indicating which files will be processed and which files will be skipped.



### **Exercise 3.3**

Add logging details for PDF documents (`pdf_to_text_with_ocr`) run to include the amount of processing time for OCR in the logs.



### **Exercise 3.4**

Identify 3 additional items (informational, debugging, etc.) that are useful to log and implement them into the code base.


### **Exercise 3.5**

Run the end-to-end script and confirm the logs reflect the updates.




<br/>

<a name="Output"/>

## 4. Output Options

In Exercise 1, we familiarized ourselves with the end-to-end pipeline, including the final output, which is to an excel file.

An excel file is a nice "quick and dirty" solution to see our outputs and to share with less-technical users. But (as developers know!), Excel is no production-level solution for storing data.

In this section, we'll add additional output data options.


### **Exercise 4.1**

Create a new python function that will transform the results into a saved pickle file. Give the user the option of where to save the file and what to call it as an input parameter to your function. Test and confirm your function works.


### **Exercise 4.2**

Use your favorite database flavor to automatically pipe the model results into a SQL table, instead of Excel or a pickle file.

We recommend `sqlalchemy` or `sqlite3` if you are working on your local machine). Feel free to leverage existing pandas capabilities to make this exercise easier! (or, go old-school and flex your SQL muscles).



### **Exercise 4.3**

Update the end-to-end pipeline function and command line arguments to enable the option of output format - Excel, pickle, or database. Test and confirm that your updated function works.





<br/>

<a name="ModelCard"/>

## 5. Model Card

As discussed in Chapter 11, model documentation is critical -  model cards provide detailed information not only about the model itself (features, algorithm, parameters), but the justification and approach. What did we try? What worked? What didn't work?

Knowing the background information is useful for anyone wanting to replicate or improve upon the existing model. It is also useful documentation for wanting to understand how the choices in model development align with the business objectives. And, it avoids unnecessary re-work for future team members who might be inclined to run the same experiments we have already completed.

Model cards also help to build a library of models over time, and can support additional activities such as ownership, governance, and responsibility. This documentation should be included with git versioning with model versions, ownership, date, etc. to tie that version of the documentation to that version of the data and model.


### **Exercise 5.1**

Create a model card! Use Figure 11.5 from the book as a helpful reference, or check out model cards online (here is the classic example from [Google](https://modelcards.withgoogle.com/)).



<br/>

<a name="InputOptions"/>

## 6. Input Options

We have our end-to-end, unit tests, our logging, and model documentation. What's missing? It's time to put together user documentation.

In many cases, our end users are going to be less technical - either subject matter experts or our product's customers. We need to make our solution as easy as possible to use and have clear documentation about how to use it.


### **Exercise 6.1**

In our simplest scenario, we would have our users leverage our solution as-is.

For this exercise, create documentation and examples to provide step-by-step instructions about how execute the pipeline.py function on a new folder of documents.

Suggestions for best practices:
- Create a .md or Word file that is simple to read
- Break it down into steps (ideally no more than 3-5 steps!)
- Use screenshots to show what good looks like for each step
- Highlight specific areas, such as what / where to click on screens
- Highlight specific items (such as filenames, paths, folders), that the user needs to change each time they want to run a new set of documents
- Show what the output should look like, if successful
- Include an initial set of "troubleshooting" or FAQs (which can be expanded on as users run into different questions or issues)
- Don't assume that users will know jargon, coding, or programs such as terminal or shell!



### **Exercise 6.2: EXTRA CREDIT**

Of course, the easiest way for less technical users to use our solution is to give them a user interface! As a "bonus" extra credit exercise, build a basic UI for your users.

The UI should have a place for users to upload a folder, and a button for them to download the results (recommend Excel).

We highly encourage use of some of the great tools out there for rapid UI development for this exercise. A production-level UI would of course need far more effort, development, and testing from an experienced UI/UX design and build team - but this is a great exercise to better understand both the UI/UX team and our user base.




<br/>

<a name="Containerize"/>

## 7. Containerize

When it comes to wrapping up and deploying a solution, containers are a great tool. They can be automated for scaling processing, scheduling jobs, for management of costs, and overall orchestration of our solution. The flexibility of container-based deployments has risen in recent years, enabling easier deployment across operating systems or cloud and on- premise platforms.

While most data scientists will work with the broader engineering team to fully containerize, deploy, and scale an NLP and AI solution, it's another helpful skill to have - both for collaboration purposes and for understanding optimization of code and environment.

In this section, the exercises here will lead us to a Docker container for our solution. **As a pre-requisite**, please make sure [Docker](https://www.docker.com/) is installed in your environment. Also refer to [Docker 101](https://www.docker.com/101-tutorial/) if you are new to Docker for the most important commands and activities.

There are many more excellent Docker resources on the internet, and also recall the encouragement to leverage LLMs to support the exercises.


### **Exercise 7.1**

Create a new folder as a working directory to package our solution into Docker. Use a lightweight Python container (e.g. [python 3.11](https://hub.docker.com/_/python) in the dropdown) as a base image.

Next, create a Dockerfile with the required packages, dependencies, and other environment variables that are needed to run our `pipeline.py` script.

For those less familiar with Docker, we have provided the following skeleton - which **will** need additional edits - to create a Dockerfile in your working directory. We recommend making the `scripts` folder your working directory, as the main `pipeline.py` script lives there.



```
# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Set the working directory inside the container
WORKDIR /<<your WD name here>>

# Install build dependencies if needed (e.g., for tesseract to run OCR locally)
RUN python -m spacy download en_core_web_sm
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final, smaller runtime image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application code
COPY . .

# Set environment variables (if needed)
# ENV OPEN_API_KEY=<<pull in your API key>>

# Define the command to run your application - this could be a UI if you've exposed a port, or could also be jupyter
CMD ["python", "pipeline.py"]
```

Note that if you did complete Exercise 6.2 to build a UI, you will also need to open a port (e.g. 8000) and add "app.py" (or similar) to the CMD option to allow an additional access point to the application/UI.



### **Exercise 7.2**

Update the Dockerfile for relevant updates:
- Ensure it pulls the latest requirements.txt file that lists all python dependencies
- Ensure that tesseract (a non-python package) is installed in the environment
- If using the OpenAI API or other LLM API, make sure the API key is accessible securely from the Dockerfile



### **Exercise 7.3**

Build the container, e.g.: `docker build -t ai-pipeline:1.0 .` and troubleshoot issues as they arise.



### **Exercise 7.4**

Use `docker run` to test and confirm that the container runs successfully - test that you can import and access python packages and functions.

Make sure you run the container while also mounting the local folder so that the container will be able to act on folders and files during processing. Check out Docker's page on [volume mounting](https://docs.docker.com/engine/storage/volumes/) if unfamiliar.

E.g. commands for mounting volumes look like the below:
`docker run -v /path/on/your/laptop/input:/app/input`

A full invocation of the pipeline script will look similar to:
```
docker run -it --rm \
    -v /path/to/your/local/input_folder:/app/input \
    -v /path/to/your/local/output_folder:/app/output \
    -v /path/to/your/local/model_folder:/app/models \
    ai-pipeline:1.0 \
    --input_folder /app/input \
    --output_folder /app/output \
    --model_folder /app/models \
    --threshold 0.6
```


### **Exercise 7.6**

Finally, let's confirm our efforts to this point are complete and functional:
- Confirm the container is built and running correctly 
- Execute the pipeline on a folder of ~10-20 documents 
- Review the output and confirm



### **Exercise 7.7: EXTRA CREDIT**

Deploy the container on your preferred cloud platform and ask a friend to test it for you!

Below are a few quickstart guides for the major cloud platforms:
- [Azure](https://learn.microsoft.com/en-us/azure/container-instances/container-instances-quickstart-portal)
- [AWS](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/)
- [GCP](https://cloud.google.com/build/docs/build-push-docker-image)

These guides will help the developer get started on deploying the containers into their preferred cloud. Following the container deployment, we recommend the following steps:
- Create a blob location for users to upload folders of documents for processing
- Update the `pipeline.py` script to pull from the blob store (optional: create a cron job (or similar cloud function - e.g. lambda function, Azure function) to check for new folder uploads and automatically trigger the pipeline script
- Update documentation with instructions for the user

<br/>



<a name="Conclusion"/>

## Conclusion

While these additional exercises here are not exhaustive, they should have given the developer a taste of the work required beyond building an AI solution in Jupyter notebooks. Notebooks are not deployable code, and there are a litany of additional steps and effort needed to turn a developed solution into a deployable solution.

In most cases (though not all!), a data scientist would not be on their  own to work through the productionalization steps, but would partner with software and cloud engineers. However, having an understanding and appreciation of the required steps is part of being a good, collaborative, cross-functional colleague and in making our broader team successful.

Additionally, not all situations call for full-scale productionalization of a solution. It's important to confer with leadership and stakeholders to understand what is truly required of a solution.

These topics are discussed in more detail in the book, particularly in chapters 10 and 11. We encourage the developer to compare their experiences with these exercises to the best practices outlined in the book.


<br/>
<br/>

<a name="About"/>

## About the Author


Rachel Wagner-Kaiser, Ph.D., has 15 years of experience in data and AI, entering the data science field after completing her Ph.D. in astronomy. She specializes in building natural language processing solutions for real-world problems constrained by limited or messy data. Rachel leads technical teams to design, build, deploy, and maintain NLP solutions, and her expertise has helped companies organize and decode their unstructured data to solve a variety of business problems and drive value through automation.


<a href="https://www.linkedin.com/in/rawagnerkaiser">
    <img src="https://i.sstatic.net/gVE0j.png" alt="Follow me on LinkedIn!"> Connect on LinkedIn
  </a>

<br /><br />




