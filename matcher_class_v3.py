from sentence_transformers import SentenceTransformer, util, CrossEncoder
import pickle
import torch
import numpy

class ResumeMatcher:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.cosine_model = 0
        self.cross_encode_model1 = 0
        self.cross_encode_model2 = 0
        self.running = True
        self.per_sentence_append_data = []

    def load_resume(self, resume_list):
        self.resume_list = resume_list

    def load_keywords(self, keywords_list):
        self.keywords_list = keywords_list

    def match(self):
        self.per_sentence_append_data = []
        self.cosine_sim_pass(self.resume_list, self.keywords_list)

        cosine_indx = torch.argsort(self.cosine_scores, descending=True)
        top_k = 9
        top_k_keywords_list = []
        top_scores_list=[]
        for i, fragment in enumerate(self.resume_list):
            top_k_keywords_list.append( [self.keywords_list[idx] for idx in cosine_indx[i][:top_k]] )
            top_scores_list.append( [self.cosine_scores[i][idx] for idx in cosine_indx[i][:top_k]] )
            ##print( cosine_indx[i][:top_k] )  ## used to affirm data alignment from previous version

        self.big_cross_encode_pass(self.resume_list, top_k_keywords_list)

        final_scores=[]
        for i in range(len(self.cross_encode_scores)):
            final_scores.append( top_scores_list[i] * self.cross_encode_scores[i] ) 


        cross_encode_indx = numpy.argsort(final_scores, axis=1)
        for i in range(len(cross_encode_indx)):
            cross_encode_indx[i] = cross_encode_indx[i][::-1]


        ##print(cross_encode_indx)

        for i, fragment in enumerate(self.resume_list):
            combined_string = " :: Potential matches :: "
            for ind in cross_encode_indx[i][:top_k]:
                combined_string += f"( {top_k_keywords_list[i][ind]} : {final_scores[i][ind]:.3f} )"


            self.per_sentence_append_data.append(combined_string)
        

    ###########################################################################

    def cosine_sim_pass(self, passed_resume, passed_keywords):
        if self.cosine_model == 0:
            print("Loading cosine pass model...")
            self.cosine_model = SentenceTransformer('all-mpnet-base-v2')
            print("Cosine pass model loaded...")

        keyword_embeddings = self.cosine_model.encode(passed_keywords)
        fragment_embeddings = self.cosine_model.encode(passed_resume)

        self.cosine_scores = util.cos_sim(fragment_embeddings, keyword_embeddings)


    def cross_encode_pass1(self, passed_resume, passed_keywords):
        if self.cross_encode_model1 == 0:
            print("Loading cross-encoder pass model...")
            self.cross_encode_model1 = CrossEncoder('cross-encoder/qnli-electra-base') # use order 2, key,frag
            print("Cross-encoder pass model loaded...")

        cross_encode_scores = []
        for i , fragment in enumerate(passed_resume):
            pairs = [(keyword, fragment) for keyword in passed_keywords[i]]
            cross_encode_scores.append( self.cross_encode_model1.predict(pairs) ) 

        return cross_encode_scores

    def cross_encode_pass2(self, passed_resume, passed_keywords):
        if self.cross_encode_model2 == 0:
            print("Loading cross-encoder pass model...")
            self.cross_encode_model2 = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2') # also use order 2, key,frag
            print("Cross-encoder pass model loaded...")

        cross_encode_scores = []
        for i , fragment in enumerate(passed_resume):
            pairs = [(keyword, fragment) for keyword in passed_keywords[i]]
            cross_encode_scores.append(  self.sigmoid(self.cross_encode_model2.predict(pairs), 0.3) )

        return cross_encode_scores
    
    def big_cross_encode_pass(self, passed_resume, passed_keywords):
        pass1 = self.cross_encode_pass1(passed_resume, passed_keywords)
        pass2 = self.cross_encode_pass2(passed_resume, passed_keywords)
        big_pass = []

        for arr in range(len(pass1)):
            big_pass.append( (1 + pass1[arr] * 0.4) * (1+ pass2[arr] *0.6) ) #### here cross entropy weights ## i forgor to document why they are those

        self.cross_encode_scores = big_pass

        
    def sigmoid(self, x, b=1):
        return 1 / (1 + numpy.exp(-x*b))
        
