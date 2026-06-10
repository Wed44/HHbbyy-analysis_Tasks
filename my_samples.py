

base_dir = "/storage/datastore-personal/kehataht/ntuples/HHbbyy_boosted_skimmed_v1"
years = ["2022", "2023", "2024"]

def make_files(prefix, encoding):
    return [f"{base_dir}/{prefix}_bbyy_{encoding}_{year}_fastsim.root" for year in years]

ggF_samples = {
    "ggF SM":            make_files("ggFHH", "SM"),
    "ggF BSM (kl = 0)":  make_files("ggFHH", "kl0"),
    "ggF BSM (kl = 10)": make_files("ggFHH", "kl10"),
}

vbf_kappa_lambda_samples = {
    "VBF SM":            make_files("VBFHH", "SM"),
    "VBF BSM (kl = 0)":  make_files("VBFHH", "kl0kvv1kv1"),
    "VBF BSM (kl = 10)": make_files("VBFHH", "kl10kvv1kv1"),
}