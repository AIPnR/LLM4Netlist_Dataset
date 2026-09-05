import os
import shutil

ARCH_NAME = 'EArch.xml'
# ARCH_NAME = 'K6_N1_fixed-layout.xml'
# ARCH_NAME = 'K4_N1_fixed-layout.xml'
DATASET = 'eval_data'

N_random_input = 200

current_dir = os.path.dirname(os.path.realpath(__file__))
arch_path = os.path.join(current_dir, 'arch_file', ARCH_NAME )

VERILOG_DATA_DIR = os.path.join(current_dir, DATASET, 'verilog_data')

VTR_OUT_DIR = os.path.join(current_dir, DATASET, 'vtr_out_'+ARCH_NAME.split('.')[0])
if os.path.exists(VTR_OUT_DIR): shutil.rmtree(VTR_OUT_DIR)
os.makedirs(VTR_OUT_DIR)

BLIF_DIR = os.path.join(current_dir, DATASET, 'blif_data_'+ARCH_NAME.split('.')[0])
if os.path.exists(BLIF_DIR): shutil.rmtree(BLIF_DIR)
os.makedirs(BLIF_DIR)

VER_DIR = os.path.join(current_dir, DATASET, 'verification_data_'+ARCH_NAME.split('.')[0])
if os.path.exists(VER_DIR): shutil.rmtree(VER_DIR)
os.makedirs(VER_DIR)



def vtr_run(vtr_out_path, verilog_path):
    vtr_run_command = '$VTR_ROOT/vtr_flow/scripts/run_vtr_flow.pl '+ verilog_path \
                    +' '+arch_path \
                    +' -temp_dir ' + vtr_out_path \
                    + ' -starting_stage odin' \
                    + ' -ending_stage prevpr' 
    os.system(vtr_run_command)


def odin_run(vtr_out_path, blif_path, N_random_input):
    odin_run_command = 'cd '+ vtr_out_path+';' \
                    + '$VTR_ROOT/ODIN_II/odin_II ' \
                    + ' -b '+blif_path \
                    + ' -g '+str(N_random_input)
    os.system(odin_run_command)

def main():
    for name in os.listdir(VERILOG_DATA_DIR)[:10]:
        design = name.split('.')[0]
        vtr_out_path = os.path.join(VTR_OUT_DIR, design) 
        os.makedirs(vtr_out_path)

        verilog_path = os.path.join(VERILOG_DATA_DIR, design+'.v')
        vtr_run(vtr_out_path, verilog_path)

        blif_path = os.path.join(vtr_out_path, design+'.pre-vpr.blif')
        odin_run(vtr_out_path, blif_path, N_random_input)

        in_vectors_path = os.path.join(vtr_out_path, 'input_vectors')
        out_vectors_path = os.path.join(vtr_out_path, 'output_vectors')
        
        if os.path.exists(blif_path) and os.path.exists(in_vectors_path) and os.path.exists(out_vectors_path):
            shutil.copy2(blif_path, BLIF_DIR)
            ver_design_dir = os.path.join(VER_DIR, design)
            os.makedirs(ver_design_dir)
            shutil.copy2(in_vectors_path, ver_design_dir)
            shutil.copy2(out_vectors_path, ver_design_dir)



if __name__ == "__main__":
    main()
