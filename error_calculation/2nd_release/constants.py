#####################################
#Parameters + constants
#####################################
D_h = 9.31e-9   # m2 / s
D_oh = 5.28e-9
D_k = 1.96e-9
D_cl = 2.04e-9
K_v = 1e-14  # mol2 / dm6
K_v = 1e-8  # mol2 / m6
k_v = 1.3e11  # dm3 / mol /s
k_v = 1.3e8 # m3 / mol / s

T = 298  # K 
K_fix = 1e-4
k_fix = 6e9
c0_fa = 4e-3   
R = 8.3145  # J / mol / K
F = 96485  # s * A / mol
epsilon = 8.8542e-12  # F / m   #vakuum
epsilon = 6.954e-10  # viz


###############################################
# EQUATION-s
###############################################

# ht = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh)
# oht = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh)
# kt = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx)
# clt = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx)
# -epsilon * phixx = F * (h-oh+k-cl-c_fa)

# res_h = D_h * hxx + D_h*F/R/T * (hx*phix + h*phixx) + k_v(K_v - h*oh) - ht
# res_oh = D_oh * ohxx - D_oh*F/R/T * (ohx*phix + oh*phixx) + k_v(K_v - h*oh) - oht
# res_k = D_k * kxx + D_k*F/R/T * (kx*phix + k*phixx) - kt
# res_cl = D_cl * clxx - D_cl*F/R/T * (clx*phix + cl*phixx) - clt
# res_poiss = F * (h-oh+k-cl-c_fa) + epsilon * phixx

# res_node = res_h^2 + res_oh^2 + res_k^2 + res_cl^2 + res_poiss^2
# res_domain = SUM(res_node)

FRT = F / R / T
K = k_v * K_v
