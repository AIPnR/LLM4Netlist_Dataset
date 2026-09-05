
import json
import os
import re
from tqdm import tqdm


def design_name_loader(load_path):
    design_name_list = []
    file_names = os.listdir(load_path)
    for file_name in file_names:
    # 使用os.path.splitext分离文件名和后缀
        name, extension = os.path.splitext(file_name)
        # 将没有后缀的文件名添加到列表中
        if 'gpt' not in name:
            design_name_list.append(name.split('.')[0]) 
        
    return design_name_list


def instruction_replace(text, key_words): #修改verilog为blif
    # 使用re.IGNORECASE使得搜索不区分大小写
    new_text = re.sub('verilog', key_words, text, flags=re.IGNORECASE)
    # 删除原文中的Please act as a professional Verilog designer.
    new_text = re.sub('Please act as a professional Verilog designer.', '', new_text, flags=re.IGNORECASE)
    return new_text


def main(dataset_name, arch_name):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    llmdata_path = os.path.join(current_dir, dataset_name+'_'+arch_name+'.json')

    BLIF_DATA_DIR = os.path.join(current_dir, dataset_name,'blif_data'+'_'+arch_name)
    # if not os.path.exists(BLIF_DATA_DIR): os.mkdir(BLIF_DATA_DIR) #创建数据集文件夹
    VERILOG_DATA_DIR = os.path.join(current_dir, dataset_name, 'verilog_data')
    INSTR_DATA_DIR = os.path.join(current_dir, dataset_name, 'instr_data')


    design_name_list = design_name_loader(BLIF_DATA_DIR)
    json_data = []
    for design_name in tqdm(design_name_list):

        blif_path = os.path.join(BLIF_DATA_DIR, design_name+'.pre-vpr.blif')
        with open(blif_path, 'r') as f:
            blif_code = ''.join([line for line in f if not line.startswith('#') and line.strip() != ''])

        verilog_path = os.path.join(VERILOG_DATA_DIR, design_name+'.v')
        with open(verilog_path, 'r') as f:
            verilog_code = ''.join([line for line in f]) 
        
        if dataset_name =='train_data':
            instr_path = os.path.join(INSTR_DATA_DIR, design_name.split('_')[0]+'.txt')
        else:
            instr_path = os.path.join(INSTR_DATA_DIR, design_name+'.txt')
        with open(instr_path, 'r') as f:
            instruction = ''.join([line for line in f]) 


        # nl_verilog_instr =      'Please write Verilog by instruction. \n'
        # nl_blif_instr =         'Please write BLIF by instruction.'
        # nl_blif_instr =         ''
        # verilog_blif_instr =    'Please syhthesis the following Verilog into BLIF. \n'

        entry = {
                    "circuit":    design_name,
                    "instr":      instruction_replace(instruction, 'BLIF'),
                    "arch":       arch_name,
                    "netlist":    blif_code,
                }
        
        json_data.append(entry)

    with open(llmdata_path, 'w') as f:
        json_data = json.dumps(json_data)
        f.write(json_data)

    with open(llmdata_path, 'r') as f:
        data = json.load(f)
        print(f"JSON 中共有 {len(data)} 条 entry。")


if __name__ == "__main__":

    dataset_name = 'train_data'
    arch_name = 'K6_N1_fixed-layout'
    main(dataset_name, arch_name)


