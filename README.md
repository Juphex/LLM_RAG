# Natural Language Processing with Word Embeddings, LLMs and RAG  

This repository implements a simple but realistic RAG pipeline with Large-Language-Models (LLMs) and experiments regarding answer generation given a question and a context. In the example, the "Formula Student Rules" are used but could be replaced by any other corpus (set of documents) or rule-set. 

## How is this project related to real-world applications?
- **Legal Documents:** For example, in the legal domain, one could use a LLM to generate answers given a question and a legal document. This could be used to automate legal research or to help lawyers find relevant information in legal documents.
- **Input Management:** In the context of input management, one could use a LLM to generate answers given a question and a set of documents. This could be used to automate the processing of incoming emails or to help customer support agents find relevant information in a knowledge base.
- **Medical Records:** In the medical domain, one could use a LLM to generate answers given a question and a patient's medical record. This could be used to automate the processing of medical records or to help doctors find relevant information in a patient's medical record.
- **Technical Documentation:** In the technical domain, one could use a LLM to generate answers given a question and a set of technical documents. This could be used to automate the processing of technical documentation or to help engineers find relevant information in technical documents.

## Formula Student Rules

The basics of the Formula Student Rules are as follows:
- The Formula Student Rules are a set of rules that are used in the Formula Student competition.
- The rules are divided into different sections, such as "Chassis", "Powertrain", "Suspension", etc.
- Each section contains a set of rules that are related to the section.
- Each rule has a unique identifier, a title, and a description.

An example of a rule is:
```markdown
# EV 7 CHARGERS

## EV 7.1 Chargers General Requirements

| EV 7.1.1 | Only chargers presented and sealed at technical inspection are allowed. All connections must be insulated and covered. No open connections are allowed. |
| EV 7.1.2 | Exposed conductive parts and the TSAC must be connected to protective earth (PE). |
| EV 7.1.3 | All components interfacing with mains must be accredited to a recognized standard e.g. CE. All remaining parts must comply with all electrical requirements for the vehicle TS. |
```

## Embeddings & Embedding Models

The notebook [WordEmbeddingSimilarities.ipynb](WordEmbeddingSimilarities.ipynb) contains code to calculate similarities between words using different embedding models. It first creates a chunk for each rule from the Formula Student Rules and then trains the embeddings. 

How it would look like as a pipeline:
```mermaid
graph LR
    subgraph "Preprocessing"
        direction LR
        A[Formula Student Rules] --> B(Create a chunk for each rule)
        B --> C(Learn Word Embedding Model)
        C --> D((Store Word Embeddings))
    end

    subgraph "Live-Querying"
        direction LR
        E[Query with Question] --> F(Compute Similarity)
        F --> D
        D --> G((Retrieve Top-k Pairs))
    end
    
    D -.-> C
    
```
### Example Query and Results
Examples show that the model is able to find suitable rules for a given question, especially when the question contains keywords that are also present in the rules:
![Alt text](/images/word_embedding_query.png)


### Limitations of embeddings:
- **Understanding:** They are not able to capture the meaning of a word or sentence in a human-like way.
- **Complexity of documents & chunks:** For this use-case, where the document chunks or Question/Answer pairs are relatively small, embeddings may retrieve rules are not directly related to the question. This is because some words may be very similar or occur often in the corpus. However, for larger documents, this problem is less likely to occur because there are more words and the embeddings are more likely to capture the meaning of the document. Also, larger documents may differ more in their content, which makes it easier for the embeddings to distinguish between them.

### Advantages of embeddings:
- **Speed & Memory:** They are very fast to compute because they are pre-trained and stored in memory.
- **Interpretability & User's attention:** This method retrieves only a top-k amount of similar rules, which can be shown to the user. First, this is more interpretable than a black-box model. Second, the user can focus on the most relevant rules and ignore the rest. Therefore, there is no "blind trust" or "black-box" problem.


## Retrieval Augmented Generation (RAG) & Large-Language-Models (LLMs)
Since the embeddings are not able to understand the meaning of a word or sentence, we can use a LLM to generate answers. The LLM can generate answers given a question and a context. The context can be the whole document or a chunk of it. The LLM can be fine-tuned on the Formula Student Rules or any other corpus.

How a basic RAG pipeline would look like:
```mermaid
graph LR
    subgraph PreprocessingLlamaIndex
        direction LR
        A[Formula Student Rules] --> B(Create Chunks)
        B --> C(Create Embeddings<br/> -HuggingFace)
        C --> D((Vector Store))
    end

    subgraph QueryingGemini
        direction LR
        E[User Question] --> F(Retrieve Relevant Chunks)
        F --> D
        D --> F
        F --> G(Construct Prompt)
        G --> H[Gemini]
        H --> I[Answer]
    end
    
    
    classDef default fill:#fff,stroke:#333,stroke-width:1px
    class A,B,C,E,F,G,H,I default
    
```

How would you validate the LLM? You could use the embeddings to retrieve the most similar rules and then compare the generated answer with the most similar rule. This way, you can see if the LLM is able to generate the correct answer given a question and a context. However, this is not a perfect evaluation because the embeddings may not retrieve the most relevant rules. Therefore, you could also use human evaluation to validate the LLM. For this case, one would use a ground-truth dataset with questions and answers and then compare the generated answers with the ground-truth answers.

```mermaid
graph LR
    subgraph ValidationProcess["Validation"]
        direction LR
        J[Ground Truth Q/A Pairs] --> K(Compare with Generated Answers)
        K --> L{Calculate Metrics}
        L --> M((Evaluation Report))
    end

    style ValidationProcess fill:#cfc,stroke:#333,stroke-width:2px 

    classDef default fill:#fff,stroke:#333,stroke-width:1px
    class A,B,C,E,F,G,H,I,J,K,L,M default

    
```