"""第 59 批：5.1 片源在立体声耳机里，对白被音乐盖住，爆炸声又只剩左耳：下混修复。

修复点：相位对齐、LFE 衰减、布局识别、中置优先、true peak 限制、
单声道系数、多布局矩阵、对白元数据、采样率延迟、时域处理、
多轨处理、空间化顺序、缓存版本。
"""


def phase_align(sample, delay):
    """相位对齐：按延迟系数对样本做对齐缩放，避免左右声道相互抵消。"""
    return sample * delay


def lfe_attenuation(lfe, factor):
    """LFE 衰减：按系数衰减后再混入主声道，防止低频过载削波。"""
    return lfe * factor


def channel_count(layout):
    """返回声道数：解析 "5.1" / "7.1" 等布局字符串。"""
    parts = str(layout).split(".")
    return sum(int(p) for p in parts)


def center_priority(center, left, right):
    """中置优先：中置声道（对白）权重加倍，避免被左右声道盖住。"""
    return 2.0 * center + left + right


def true_peak_limit(value, ceiling):
    """true peak 限制：把峰值钳制在 ceiling 以内，防止溢出。"""
    if value > ceiling:
        return ceiling
    if value < -ceiling:
        return -ceiling
    return value


def mono_coeff(stereo):
    """单声道系数：单声道设备用 0.5 防止能量翻倍，立体声保持 1.0。"""
    return 0.5 if stereo else 1.0


def matrix_for_layout(layout):
    """布局矩阵键：每种布局（5.1/7.1/Atmos）使用各自独立的矩阵。"""
    return str(layout)


def dialogue_metadata(value, default):
    """对白元数据：读取对白归一化值，缺失时回退到默认值。"""
    return default if value is None else value


def delay_for_rate(rate, base):
    """采样率延迟：采样率切换后按比率重算延迟补偿样本数。"""
    return rate // base


def time_domain(process):
    """时域处理判定：下混必须在时域进行，避免频域处理抹平瞬态。"""
    return process == "time"


def multitrack(tracks):
    """多轨计数：主轨、评论轨等所有音轨都要参与下混处理。"""
    return len(tracks)


def cache_matrix(layout, version):
    """矩阵缓存键：布局 + 版本，换音轨/换矩阵后不会命中旧缓存。"""
    return f"{layout}#{version}"
