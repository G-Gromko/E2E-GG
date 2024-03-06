from utils import levenshtein

def parse_krn_content(krn, ler_parsing=False, cer_parsing=False):
    if cer_parsing:
        krn = krn.replace("\n", " <b> ")
        krn = krn.replace("\t", " <t> ")
        tokens = krn.split(" ")
        characters = []
        for token in tokens:
            if token in ['<b>', '<t>']:
                characters.append(token)
            else:
                for char in token:
                    characters.append(char)
        return characters
    elif ler_parsing:
        krn_lines = krn.split("\n")
        for i, line in enumerate(krn_lines):
            line = line.replace("\n", " <b> ")
            line = line.replace("\t", " <t> ")
            krn_lines[i] = line
        return krn_lines
    else:
        krn = krn.replace("\n", " <b> ")
        krn = krn.replace("\t", " <t> ")
        return krn.split(" ")

def compute_metric(a1, a2):
    acc_ed_dist = 0
    acc_len = 0

    for (h, g) in zip(a1, a2):
        acc_ed_dist += levenshtein(h, g)
        acc_len += len(g)

    return 100.*acc_ed_dist / acc_len

def get_metrics(hyp_array, gt_array):
    hyp_cer = []
    gt_cer = []

    hyp_ser = []
    gt_ser = []

    hyp_ler = []
    gt_ler = []

    for h_string, gt_string in zip(hyp_array, gt_array):
        hyp_ler.append(parse_krn_content(h_string, ler_parsing=True, cer_parsing=False))
        gt_ler.append(parse_krn_content(gt_string, ler_parsing=True, cer_parsing=False))

        hyp_ser.append(parse_krn_content(h_string, ler_parsing=False, cer_parsing=False))
        gt_ser.append(parse_krn_content(gt_string, ler_parsing=False, cer_parsing=False))

        hyp_cer.append(parse_krn_content(h_string, ler_parsing=False, cer_parsing=True))
        gt_cer.append(parse_krn_content(gt_string, ler_parsing=False, cer_parsing=True))

    acc_ed_dist = 0
    acc_len = 0

    cer = 0
    ser = 0
    ler = 0

    for (h, g) in zip(hyp_cer, gt_cer):
        acc_ed_dist += levenshtein(h, g)
        acc_len += len(g)

    cer = compute_metric(hyp_cer, gt_cer)
    ser = compute_metric(hyp_ser, gt_ser)
    ler = compute_metric(hyp_ler, gt_ler)

    return cer, ser, ler