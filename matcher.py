"""
guided text rewriting or controlled text generation/editing.

Modifying text	Text editing / controlled generation
Improving alignment to keywords	Semantic similarity / keyword coverage
Comparing keywords to text	Text-keyword matching or similarity scoring

"""
import pickle
import torch
from sentence_transformers import SentenceTransformer, util

def match_resume_to_job(resume, job_description):
    list_fragments = preprocess_resume(resume)
    list_keywords = preprocess_job_description(job_description)

    model = SentenceTransformer('all-MiniLM-L6-v2') ## currently  all-MiniLM-L6-v2; swap all-mpnet-base-v2 when ready

    try:
        with open("embeddings_cache.pkl", "rb") as f:
            keyword_embeddings, fragment_embeddings = pickle.load(f)
    except FileNotFoundError:
        list_fragments = preprocess_resume(resume)
        list_keywords = preprocess_job_description(job_description)

        keyword_embeddings = model.encode(list_keywords)
        fragment_embeddings = model.encode(list_fragments)

        with open("embeddings_cache.pkl", "wb") as f:
            pickle.dump((keyword_embeddings, fragment_embeddings), f)


    cosine_scores = util.cos_sim(fragment_embeddings, keyword_embeddings)  ## sensitive to non-keyword type words

    

    for i, fragment in enumerate(list_fragments):
        sorted_idx = torch.argsort(cosine_scores[i], descending=True)
        for idx in sorted_idx[:5]:
            print( f"( {fragment} -> {list_keywords[idx]} : {cosine_scores[i][idx].item():.3f} )" )
            ## for each fragment in list_fragments, append {list_keywords[idx] : cosine_scores[i][idx].item():.2f}

    #selected_indices = torch.topk(cosine_scores, k=5, dim=1)[1]
    #selected_fragments = torch.gather(torch.tensor(list_fragments), 0, selected_indices)

    # max_similarity_per_fragment = cosine_scores.max(dim=1)[0]

    #for fragment, similarity in zip(list_fragments, max_similarity_per_fragment):
    #    print(fragment, similarity, float(similarity))

    '''
    top_keywords_per_fragment = cosine_scores[selected_indices].argmax(dim=1)
    for frag, kw_idx in zip(selected_fragments, top_keywords_per_fragment):
        top_keyword = list_keywords[kw_idx]
        print(f"Fragment: {frag}")
        print(f"Top matching keyword: {top_keyword}")
        '''
    
        
    pass

def preprocess_resume(resume):
    list_fragments = []
    for entry in resume.get("work_history").get("entries"):
        list_fragments.append(entry.get("summary"))
        for experience in entry.get("experiences"):
            #list_fragments.append( f"{experience.get('what')} , {experience.get('how')} , {experience.get('result')}" )
            list_fragments.append( experience.get('what') )
            list_fragments.append( experience.get('how') )
            list_fragments.append( experience.get('result') )

    return list_fragments

def preprocess_job_description(job_description):
    return job_description