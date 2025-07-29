from sentence_transformers import SentenceTransformer
import faiss
import torch
import pickle


def search_sentence_in_faiss(sentence):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("spl_faiss.index")
    with open("spl_data_mapping.pkl", "rb") as f:
        spl = pickle.load(f)
    with open("xql_data_mapping.pkl", "rb") as f:
        xql = pickle.load(f)

    # Encode a new raw log
    query_embedding = model.encode([sentence], convert_to_numpy=True)

    # Search
    top_k = 3
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve matched data_model(s)
    results = []
    for idx in indices[0]:
        results.append((spl[idx], xql[idx]))
    return results



if __name__ == "__main__":
    print(search_sentence_in_faiss("""Jul 29 12:16:26 2024-07-29 04: 16:57 12 10.141.6.69 206 TCP_NC_MISS 131714 408 GET http swdc02-mscdn.manage.microsoft.com 80 /5d909be8-cdb0-4028-89d4-a8898e73f6f9/62837087-93f0-4166-b256-25861bf9270b/a4f5e21a-cd1f-402a-a00d-ba7bde3ad1a8.intunewin.bin - - - - swdc02-mscdn.manage.microsoft.com application/octet-stream - "Microsoft-Delivery-Optimization/10.0" OBSERVED "ITSD_URL;ProjectHarmony_URL;Peacock User Whitelist;URLRequest;Visual Studio Whitelist;O365Urls;Peacock URL;DEV_UAT;NPS URL;Cloud VDI URL whitelist;Intune2URL;HCI PILOT URL;Exchange 2016 URL;UnifyCloud URL;MDATP;DPM;HCI POC Azure Portal;MSActivation;All AccessYes URL;Permitted Sites;PowerBI_URL;COS url;Sudong_MCC_KCC;Innovax URL;GEIM Tenant_URL;AmdocsApprovedURLs;MCCStandardWhitelistSites;Xenapps Allowed URLs;Peacock Automation;HybridJoin-Azure;Permitted CCO Sites;Intune URL;URLfor SCCM Server Access;GeneralWhitelistedURL;IntuneAutopilotServer Url;O365URL;Technology/Internet" - 172.16.35.227 80"""))