NEURON {
  SUFFIX leak
  NONSPECIFIC_CURRENT i
  RANGE i, e, g
}

PARAMETER {
  g = 1e-5 (siemens/cm2)
  e = -65 (millivolt)
}

ASSIGNED {
  i (milliamp/cm2)
  v (millivolt)
}

BREAKPOINT {
  i = g*(v - e)
}
