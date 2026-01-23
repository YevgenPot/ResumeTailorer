from sentence_transformers import SentenceTransformer, util
import pickle
import torch


class ResumeMatcher:
    def __init__(self, model_name='all-mpnet-base-v2'):
        print("Loading model...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded!")
        self.running = True

    def load_resume(self, resume_list):
        self.resume_list = resume_list

    def load_keywords(self, keywords_list):
        self.keywords_list = keywords_list

    def match(self):
        keyword_embeddings = self.model.encode(self.keywords_list)
        fragment_embeddings = self.model.encode(self.resume_list)

        '''
        try:
            with open("embeddings_cache.pkl", "rb") as f:
                keyword_embeddings, fragment_embeddings = pickle.load(f)
        except FileNotFoundError:
            keyword_embeddings = self.model.encode(keywords)
            fragment_embeddings = self.model.encode(fragments)
            with open("embeddings_cache.pkl", "wb") as f:
                pickle.dump((keyword_embeddings, fragment_embeddings), f)
        '''

        cosine_scores = util.cos_sim(fragment_embeddings, keyword_embeddings)


        top_k = 4 #hparam
        append_scores_list = []
        for i, fragment in enumerate(self.resume_list):
            temp_k = top_k
            sorted_idx = torch.argsort(cosine_scores[i], descending=True)
            for idx in sorted_idx[:top_k]:
                if self.keywords_list[idx] in fragment:
                    cosine_scores[i][idx] = 0.999
                    temp_k += 1

            '''
            Recommended Next Step for You:

Implement a sliding window + merge/expand around literal matches first.

Compute cosine similarity for each window.

Pick the window with the max similarity and store that as the fragment-keyword match.
            '''

            sorted_idx = torch.argsort(cosine_scores[i], descending=True)
            combined_string = ".  _[Potential Matches]_ -> "
            for idx in sorted_idx[:temp_k]:
                combined_string += f" ({self.keywords_list[idx]} : {cosine_scores[i][idx].item():.2f})" # testing append cosine scores
                #combined_string += f" ({self.keywords_list[idx]})"
            append_scores_list.append(combined_string)                

        self.scores_list = append_scores_list


## potentially make a mergse sort style cosine_sim maker

'''
    def run_loop(self):
        while self.running:
            resume = input("Paste resume (or 'quit'): ") ## file name DOT file type
            if resume.lower() == 'quit':
                self.turn_off()
                break
            job_description = input("Paste job description: ")
            results = self.match(resume, job_description)
            for m in results:
                print(m["fragment"], m["similarity"])

    def turn_off(self):
        self.running = False
        print("Matcher stopped.")

        '''
