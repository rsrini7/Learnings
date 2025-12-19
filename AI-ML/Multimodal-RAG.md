# Multimodal RAG Approaches

This document explores how multimodal RAG extends traditional RAG to include various media types like images, video, and audio.

Key topics covered include:

*   An explanation of how multimodal RAG works by retrieving information from diverse sources such as audio, images, and text, and then using this information to generate responses.
*   Discussions on different approaches to multimodal RAG:
    *   **Joint Embedding:** Using a single model to encode different data types into a shared vector space.
    *   **Grounded Modality:** Converting all data types into a single modality, typically text, before encoding.
    *   **Multiple Encoders:** Employing several different encoding models for specific modality pairs and combining and re-ranking the results.
*   Practical considerations, challenges, and trade-offs of each approach.

---

Based on the three provided flow images, here's a combined detailed description of the different approaches to multimodal Retrieval Augmented Generation (RAG) they depict:

The core concept illustrated across all three diagrams is the process of using a knowledge base (Docstore) to retrieve relevant information in response to a user query and then using that information to augment the generation of a response. The key difference lies in how the multimodal data within the Docstore and the user query are processed and encoded before retrieval.

## Flow 1: Separate Multimodal Encoding (Image 1)

This flow represents an approach where different modalities (audio, image, text) are encoded into vectors independently but within a shared vector space.

1.  **Docstore:** Contains a variety of data types including audio, images, and text documents.
2.  **User Query:** A query from the user, which can also be in text format (e.g., "What Color is the Eiffel Tower?").
3.  **Encoding:**
    *   Content from the Docstore is passed through respective encoding modules: "Audio Encoding," "Image Encoding," and "Text Encoding." Each encoder converts its specific modality into a vector representation that captures its meaning.
    *   The User Query (if text) is also processed by the "Text Encoding" module.
4.  **Vector Space Representation:** The resulting vectors from all encoding processes are plotted in a multidimensional vector space. In this space, vectors representing semantically similar content, regardless of their original modality, are located closer to each other.
5.  **Retrieval:** Using the vector representation of the User Query, a search is performed within the vector space to find the most similar vectors corresponding to data in the Docstore. This step, labeled "Retrieval," aims to "Find Data Relevant to the Query."
6.  **Augment and Generate:** The data associated with the retrieved relevant vectors is then used to "Augment" the information available to a generation model, which then produces a response to the user query.

## Flow 2: Grounded Modality / Conversion to Text (Image 2)

This flow illustrates an approach where non-text modalities are converted into text before encoding and retrieval.

1.  **Docstore:** Contains audio, images, and text documents.
2.  **User Query:** A text query (e.g., "What Color is the Eiffel Tower?").
3.  **Conversion to Text:**
    *   Audio data from the Docstore is processed by an "Audio to Text" model to generate a textual description.
    *   Image data from the Docstore is processed by an "Image to Text" model (like an image captioning model) to generate a textual description.
    *   Text documents remain as text.
4.  **Text Encoding:** All the resulting text data (converted audio/image text and original text documents) is then processed by a single "Text Encoding" module, converting it into vectors. The User Query is also processed by this Text Encoding module.
5.  **Vector Space Representation:** The text-encoded vectors are represented in a vector space.
6.  **Retrieval:** Similar to the first flow, the User Query vector is used to find the most relevant text-encoded data vectors from the Docstore in the vector space. This step is also labeled "Retrieval - Find Data Relevant to the Query."
7.  **Augment and Generate:** The retrieved text data is used to "Augment" and "Generate" the final response.

## Flow 3: Multiple Encoders with Re-Ranking (Image 3)

This flow presents a more sophisticated approach that uses multiple specialized encoders and adds a re-ranking step to improve retrieval accuracy.

1.  **Docstore:** Contains audio, images, and text documents.
2.  **User Query:** A text query (e.g., "What Color is the Eiffel Tower?").
3.  **Encoding with Aligned Models:** This flow utilizes specialized models aligned for specific modality pairs:
    *   **Audio/Text Aligned Model:** Processes audio and text, with separate "Audio Encoding" and "Text Encoding" components.
    *   **Image/Text Aligned Model:** Processes images and text, with separate "Image Encoding" and "Text Encoding" components.
    *   There is also a separate "Text Encoding" path for handling text documents or the text query directly.
    *   These encoders convert the data into vectors within potentially different or aligned vector spaces. The User Query is typically encoded via the relevant text encoding paths.
4.  **Retrieval:** Multiple parallel "Retrieval" steps occur based on the outputs of the different encoding paths, finding data relevant to the query within each respective modality's encoded space.
5.  **Re-Rank:** The results from the multiple retrieval steps are passed to a "Re-Rank" component. This system compares the retrieved content across modalities and decides which pieces of information are most useful and relevant to the original user query. This step helps to synthesize and prioritize information from different sources.
6.  **Augment and Generate:** The re-ranked and prioritized data is then used to "Augment" the generation model, leading to the final generated response.

## Combined Summary

In essence, these three flows demonstrate different strategies for building multimodal RAG systems:

*   **Separate Encoding:** Encodes each modality independently into a shared space.
*   **Grounded Modality:** Converts non-text data to text before encoding and retrieval, leveraging existing text-based RAG techniques.
*   **Multiple Encoders with Re-Ranking:** Uses specialized encoders for different modality combinations and incorporates a re-ranking step to refine the retrieval results from multiple sources.

All three approaches share the fundamental steps of processing data from a Docstore and a User Query, performing a retrieval step to find relevant information, and finally using this retrieved information to augment a generation process to produce a comprehensive response to the user's query, leveraging the power of multimodal data. The choice of approach depends on factors like the nature of the data, desired complexity, and performance requirements.

It looks like you've shared three images that visually represent the three different approaches to multimodal Retrieval Augmented Generation (RAG) discussed in the Rag Masters episode you previously watched. Let's break down the video's explanation alongside these visual flows:

### Overall Concept of Multimodal RAG

The core idea of multimodal RAG, as highlighted in the video [[00:39](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=39)], is to extend the capabilities of traditional RAG (which primarily deals with text) to incorporate various data modalities like audio, images, and video. This allows the system to retrieve and utilize information from a richer set of sources when answering a user's query.

The general process involves:

1.  **Docstore:** A repository containing data in different formats (text documents, audio files, images, video).
2.  **User Query:** The question or prompt from the user.
3.  **Encoding/Transformation:** Converting the data from the docstore and the user query into a format suitable for comparison (typically vector embeddings). This is where the three approaches differ significantly.
4.  **Retrieval:** Finding the data in the docstore that is most relevant to the encoded user query based on similarity in the embedding space.
5.  **Augment:** Combining the retrieved information with the original user query.
6.  **Generate:** Feeding the augmented prompt to a multimodal model to generate the final response.

Now, let's delve into the three approaches, comparing the video's explanation with the visual representations in your images:

### Approach 1: Joint Embedding (Image 1)

*   **Video Explanation:** The video describes joint embedding [[05:40](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=340)] as using a single multimodal model to encode different data types (audio, images, text) into a unified vector space [[06:22](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=382)]. The user query is also embedded into this same space, and retrieval happens by finding the closest vectors [[06:52](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=412)].

*   **Image 1 Breakdown:**
    *   The diagram shows a **Docstore** containing various data types.
    *   The **User Query** ("What Color is the Eiffel Tower?") is shown as text.
    *   There are separate **Encoding** blocks for Audio, Image, and Text. Each converts its respective data type into a vector representation (indicated by the colored bars). Crucially, these vectors are designed to exist in the same embedding space.
    *   The encoded query and the encoded data from the docstore are represented as points in a 2D vector space.
    *   **Retrieval** is depicted as selecting the data points (representing relevant audio, images, or text) that are closest to the query point (inside the red circle).
    *   Finally, the retrieved information is used to **Augment** the query before being passed to the **Generate** step.

### Approach 2: Grounded Modality (Image 2)

*   **Video Explanation:** This approach, as explained in the video [[11:13](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=673)], involves converting all non-text data (audio, images) into text [[11:48](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=708)]. Then, a standard text encoding model is used to create embeddings for this text, and retrieval is performed based on the text query in the text embedding space [[11:54](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=714)].

*   **Image 2 Breakdown:**
    *   Similar to Image 1, there's a **Docstore** and a **User Query**.
    *   The key difference lies in the transformation step. Instead of directly encoding audio and images into a shared vector space, there are "Audio to Text" and "Image to Text" modules. These modules use models to generate textual descriptions of the audio and images.
    *   All data, including the original text and the generated text from audio and images, is then passed through a **Text Encoding** module to create vector embeddings.
    *   The retrieval process happens in this text-based vector space, finding textually relevant information.
    *   The retrieved text is then used for **Augmentation** and finally **Generation**.

### Approach 3: Multiple Encoders (Image 3)

*   **Video Explanation:** The video details the multiple encoders approach [[17:19](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=1039)] as using separate encoding models tailored for different modalities [[18:07](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=1087)]. This results in multiple retrieval steps, one for each modality (or combination of modalities) [[18:48](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=1128)]. The retrieved results are then often ranked or combined before being used for generation [[19:08](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=1148)].

*   **Image 3 Breakdown:**
    *   Again, we see the **Docstore** and **User Query**.
    *   There are multiple encoding pipelines:
        *   **Audio/Text Aligned Model:** Encodes both audio and text using models that aim to align their embeddings.
        *   **Image/Text Aligned Model:** Encodes both images and text with the goal of alignment.
        *   **Text Encoding:** Encodes text independently.
    *   Each encoding pipeline has its own **Retrieval** step, potentially in different vector spaces.
    *   The retrieved results from these multiple retrievals are then fed into a **Re-Rank** system. This system evaluates the relevance and importance of the retrieved content from different modalities.
    *   The re-ranked and combined information is then used for **Augmentation** and finally **Generation**.

## Key Takeaways from the Video and the Flows:

*   **Flexibility vs. Integration:** The video discusses the trade-off between the flexibility of using specialized models for each modality (Multiple Encoders) and the potential simplicity and efficiency of a single, integrated model (Joint Embedding) [[23:39](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=1419)]. Grounded Modality offers a way to leverage existing text-based RAG infrastructure.
*   **Use Case Dependence:** The best approach is not universal and depends on the specific application, the types of data involved, and the desired performance characteristics [[14:13](http://www.youtube.com/watch?v=ZetGV7gtyQw&t=853)].
*   **Complexity:** The Multiple Encoders approach appears the most complex, involving multiple encoding and retrieval stages, as well as a re-ranking mechanism.
*   **Evolution of RAG:** The video highlights how RAG is evolving beyond just text to handle the richness of real-world data.

These visual flows effectively illustrate the core differences in how each multimodal RAG approach handles the encoding and retrieval of information from diverse data sources, aligning well with the explanations provided in the Rag Masters episode.

Ref: [https://gist.github.com/rsrini7/f006562092078bc0d6e1254041970e34](https://gist.github.com/rsrini7/f006562092078bc0d6e1254041970e34)