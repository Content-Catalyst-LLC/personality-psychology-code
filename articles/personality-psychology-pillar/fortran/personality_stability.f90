program personality_stability
  implicit none

  integer :: t
  real :: organization
  real, parameter :: stability = 0.72
  real, parameter :: regulation = 0.68
  real, parameter :: pressure = 0.25
  real, parameter :: rate = 0.06

  organization = 0.45

  print *, "Time", "Organization"

  do t = 1, 12
     organization = organization + rate * (stability + regulation - pressure)
     if (organization > 1.0) organization = 1.0
     if (organization < 0.0) organization = 0.0
     print *, t, organization
  end do

end program personality_stability
