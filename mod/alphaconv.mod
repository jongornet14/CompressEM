NEURON {
  POINT_PROCESS AlphaConvol
  POINTER Vpre
  RANGE e,i,k,g,tau_g,a
  NONSPECIFIC_CURRENT i
}

PARAMETER {
  e = 0         (mV)
  k = 5e-5      (uS)
  tau_a = 1e-6  (ms)
}

ASSIGNED {
  v     (mV)
  Vpre  (mV)
  i     (nA)
  g
}

STATE { a (microsiemens) }

INITIAL {
  a = 0
}

BREAKPOINT {
  SOLVE state METHOD cnexp
  g = k*(Vpre+65)
  i = g^2*(v-e) + a^2*(v+65)
}

DERIVATIVE state {
  a' = tau_a*(Vpre+65)
}
