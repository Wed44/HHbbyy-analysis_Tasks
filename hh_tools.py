import uproot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


FILES_3YEARS = [
    "/storage/datastore-personal/kehataht/ntuples/HHbbyy_boosted_skimmed_v1/ggFHH_bbyy_SM_2022_fastsim.root",
    "/storage/datastore-personal/kehataht/ntuples/HHbbyy_boosted_skimmed_v1/ggFHH_bbyy_SM_2023_fastsim.root",
    "/storage/datastore-personal/kehataht/ntuples/HHbbyy_boosted_skimmed_v1/ggFHH_bbyy_SM_2024_fastsim.root",  ]

def plot_kinematics(
    files, 
    x_variable='pt_bb', 
    title="Kinematics Plot", 
    bins=50,
    xlim=None,          
    ylim=(0, 5),        
    log_scale=True,     
    draw_dr_line=True,  
    save_name=None      
):
    
    
    dR_values = []
    x_values = []
    weights = []

    for filepath in files:
        with uproot.open(filepath) as file:
            tree = file["AnalysisMiniTree"]
            
            branches = [
                "truth_children_fromH1_pdgId", "truth_children_fromH2_pdgId",
                "generatorWeight_NOSYS", 
                "truth_children_fromH1_eta", "truth_children_fromH1_phi",
                "truth_children_fromH2_eta", "truth_children_fromH2_phi"
            ]
            if x_variable in ['pt_bb', 'pt_yy']: branches += ["truth_H1_pt", "truth_H2_pt"]
            if x_variable == 'm_hh': branches += ["truth_HH_m"]
                
            arrays = tree.arrays(branches, library="np")

            
            for i in range(len(arrays["truth_children_fromH1_pdgId"])):
                is_H1_bb = 5 in arrays["truth_children_fromH1_pdgId"][i]
                
                # Safety check 
                if is_H1_bb and len(arrays["truth_children_fromH1_eta"][i]) < 2: continue
                if not is_H1_bb and len(arrays["truth_children_fromH2_eta"][i]) < 2: continue

                if is_H1_bb:
                    deta = arrays["truth_children_fromH1_eta"][i][0] - arrays["truth_children_fromH1_eta"][i][1]
                    dphi = arrays["truth_children_fromH1_phi"][i][0] - arrays["truth_children_fromH1_phi"][i][1]
                else:
                    deta = arrays["truth_children_fromH2_eta"][i][0] - arrays["truth_children_fromH2_eta"][i][1]
                    dphi = arrays["truth_children_fromH2_phi"][i][0] - arrays["truth_children_fromH2_phi"][i][1]
                
                dphi = (dphi + np.pi) % (2 * np.pi) - np.pi
                dR = np.sqrt(deta**2 + dphi**2)
                
                if x_variable == 'pt_bb':
                    x_val = (arrays["truth_H1_pt"][i] if is_H1_bb else arrays["truth_H2_pt"][i]) / 1000.0
                elif x_variable == 'pt_yy':
                    x_val = (arrays["truth_H2_pt"][i] if is_H1_bb else arrays["truth_H1_pt"][i]) / 1000.0
                elif x_variable == 'm_hh':
                    x_val = arrays["truth_HH_m"][i] / 1000.0
                
                dR_values.append(dR)
                x_values.append(x_val)
                weights.append(arrays["generatorWeight_NOSYS"][i])

    
    plt.figure(figsize=(8, 6))
    
    norm = LogNorm() if log_scale else None
    
    plt.hist2d(x_values, dR_values, bins=bins, weights=weights, cmap="viridis", norm=norm)
    plt.colorbar(label="weighted events")
    
    if x_variable in ['pt_bb', 'pt_yy']: 
        plt.xlabel(f"pT({'bb' if x_variable == 'pt_bb' else 'yy'}) [GeV]")
        if xlim is None: xlim = (0, 1000) 
    elif x_variable == 'm_hh': 
        plt.xlabel("mHH [GeV]")
        if xlim is None: xlim = (250, 1000) 
    
    plt.ylabel("ΔR(bb)")
    plt.title(title)
    
    plt.xlim(xlim)
    plt.ylim(ylim)
    
    if draw_dr_line:
        plt.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='ΔR(bb) = 1')
        plt.legend()
        
    
    if save_name:
        plt.savefig(save_name, dpi=300, bbox_inches='tight')
        print(f"Plot saved to hard drive as: {save_name}")
        
        
        
        
        
        
        
        
        
def plot_kin(ax, files, x_variable='pt_bb', title='pinkie', bins=50, x_lim=None, y_lim=(0, 5), log_scale=True, draw_dr_line=True):
    
    dR_values = []
    x_values = []
    weights = []

    # 1. Open files and extract data (Exactly the same as before)
    for filepath in files:
        with uproot.open(filepath) as file: 
            tree = file['AnalysisMiniTree']
            branches = ["bbyy_dRbb_NOSYS", "generatorWeight_NOSYS"]

            if x_variable == "m_hh": branches.append("bbyy_mbbyy_star_NOSYS")
            elif x_variable == "pt_bb": branches.append("bbyy_pTbb_NOSYS")
            elif x_variable == "pt_yy": branches.append("bbyy_pTyy_NOSYS")

            arrays = tree.arrays(branches, library='np')
            dr = arrays["bbyy_dRbb_NOSYS"]
            weight = arrays["generatorWeight_NOSYS"]

            if x_variable == "m_hh": x = arrays["bbyy_mbbyy_star_NOSYS"] / 1000.0
            elif x_variable == "pt_bb": x = arrays["bbyy_pTbb_NOSYS"] / 1000.0
            elif x_variable == "pt_yy": x = arrays["bbyy_pTyy_NOSYS"] / 1000.0

            dR_values.extend(dr)
            x_values.extend(x)
            weights.extend(weight)

    # 2. Draw on the specific 'ax' (box) we provide!
    norm = LogNorm() if log_scale else None
    
    # We save the drawing as 'mesh' so we can attach a colorbar specifically to this box
    mesh = ax.hist2d(x_values, dR_values, bins=bins, weights=weights, cmap="viridis", norm=norm)
    plt.colorbar(mesh[3], ax=ax, label="weighted events")
    
    if x_variable in ['pt_bb', 'pt_yy']: 
        ax.set_xlabel(f"pT({'bb' if x_variable == 'pt_bb' else 'yy'}) [GeV]")
        if x_lim is None: x_lim = (0, 1000) 
    elif x_variable == 'm_hh': 
        ax.set_xlabel("m*HH [GeV]") 
        if x_lim is None: x_lim = (250, 1000) 
    
    ax.set_ylabel("ΔR(bb)")
    ax.set_title(title)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    
    if draw_dr_line:
        ax.axhline(y=1.0, color='red', linestyle='--', linewidth=1.5, label='ΔR(bb) = 1')
        ax.legend(loc='upper right')
        
        
        
        
        
        
base_dir = "/storage/datastore-personal/kehataht/ntuples/HHbbyy_boosted_skimmed_v1"
years = ["2022", "2023", "2024"]


background_samples = {
    "yybb":    (["yybb"], "fastsim"),
    "yyjets":  (["yyjets"], "fastsim"),
    "ttyy":    (["ttyy_allhad", "ttyy_nonallhad"], "fullsim"),
    "ggFH":    (["ggFH_yy"], "fullsim"),
    "VBFH":    (["VBFH_yy"], "fullsim"),
    "ttH":     (["ttH_yy"], "fullsim"),
    "ggZH":    (["ggZH_yy"], "fullsim"),
    "qqZH":    (["qqZH_yy"], "fullsim"),
    "WmH":     (["WmH_yy"], "fullsim"),
    "WpH":     (["WpH_yy"], "fullsim"),
    "tHjb":    (["tHjb_yy"], "fullsim"),
    "tWH":     (["tWH_yy"], "fullsim"),
    "bbH":     (["bbH_yy"], "fullsim"),
    "bbH_yt2": (["bbH_yt2_yy"], "fullsim"),}

variables = ['pt_bb', 'm_hh']   

for name, (prefixes, simtype) in background_samples.items():
    file_list = []
    for prefix in prefixes:
        for year in years:
            file_list.append(f"{base_dir}/{prefix}_{year}_{simtype}.root")

    if not all(os.path.exists(f) for f in file_list):
        print(f"Skipping {name} - not all files exist.")
        continue

    print(f"\nProcessing background: {name}")

    for var in variables:
        if var == 'pt_bb':
            plot_title = f"ΔR(bb) vs pT(bb) — Background: {name}"
            save_name = f"bg_ptbb_{encoding}.png"
        elif var == 'm_hh':
            plot_title = f"ΔR(bb) vs m*bbγγ — Background: {name}"
            save_name = f"bg_m*bbyy_{encoding}.png"
        elif var == 'pt_yy':
            plot_title = f"ΔR(bb) vs pT(yy) — Background: {name}"
            save_name = f"bg_ptyy_{encoding}.png"

        plot_kin(files=file_list, x_variable=var, title=plot_title)
        
    plt.show()