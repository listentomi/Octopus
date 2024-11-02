from typing import Dict
import pandas as pd
import os

def power_query_types() -> Dict[str, int]:
    #df = pd.read_excel(r'data\spider\simple.xlsx')
    df = pd.read_excel(r'data\spider\level_5.xlsx')
    res = df.set_index('template')['weight'].to_dict()
    #res = {'Root1(3) Root(3) Sel(1) N(0) A(0) Op(0) C(11) T(5) C(11) T(5) Filter(0) Filter(2) A(0) Op(0) C(4) T(1) C(4) T(1) V(0) Filter(0) Filter(2) A(0) Op(0) C(10) T(4) C(10) T(4) V(1) Filter(0) Filter(2) A(0) Op(0) C(13) T(5) C(13) T(5) V(2) Filter(2) A(0) Op(0) C(2) T(0) C(2) T(0) V(3)':1}
    return res

def complex_query_types() -> Dict[str, int]:
    #df = pd.read_excel(r'data\spider\simple.xlsx')
    df = pd.read_excel(os.path.join('.','template','complex.xlsx'),engine='openpyxl')
    res = df.set_index('template')['weight'].to_dict()
    #res = {'Root1(3) Root(3) Sel(1) N(0) A(0) Op(0) C(11) T(5) C(11) T(5) Filter(0) Filter(2) A(0) Op(0) C(4) T(1) C(4) T(1) V(0) Filter(0) Filter(2) A(0) Op(0) C(10) T(4) C(10) T(4) V(1) Filter(0) Filter(2) A(0) Op(0) C(13) T(5) C(13) T(5) V(2) Filter(2) A(0) Op(0) C(2) T(0) C(2) T(0) V(3)':1}
    return res

def simple_query_types() -> Dict[str, int]:
    #df = pd.read_excel(r'data\spider\simple.xlsx')
    df = pd.read_excel(os.path.join('.','template','simple.xlsx'),engine='openpyxl')
    res = df.set_index('template')['weight'].to_dict()
    #res = {'Root1(3) Root(3) Sel(1) N(0) A(0) Op(0) C(11) T(5) C(11) T(5) Filter(0) Filter(2) A(0) Op(0) C(4) T(1) C(4) T(1) V(0) Filter(0) Filter(2) A(0) Op(0) C(10) T(4) C(10) T(4) V(1) Filter(0) Filter(2) A(0) Op(0) C(13) T(5) C(13) T(5) V(2) Filter(2) A(0) Op(0) C(2) T(0) C(2) T(0) V(3)':1}
    return res