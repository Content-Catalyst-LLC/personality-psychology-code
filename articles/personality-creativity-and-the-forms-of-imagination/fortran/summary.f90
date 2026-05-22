program personality_creativity_summary
  implicit none
  integer :: unit, ios, n, id
  character(len=512) :: header
  character(len=32) :: domain
  real :: openness, intellect, conscientiousness, extraversion, agreeableness
  real :: neuroticism, persistence, social_support
  real :: divergent_thinking, creative_achievement, everyday_creativity
  real :: openness_sum, achievement_sum

  openness_sum = 0.0
  achievement_sum = 0.0
  n = 0

  open(newunit=unit, file='../data/synthetic_personality_creativity.csv', status='old', action='read', iostat=ios)
  if (ios /= 0) stop 'could not open data file'

  read(unit, '(A)') header
  do
    read(unit, *, iostat=ios) id, openness, intellect, conscientiousness, extraversion, agreeableness, &
      neuroticism, persistence, social_support, domain, divergent_thinking, creative_achievement, everyday_creativity
    if (ios /= 0) exit
    openness_sum = openness_sum + openness
    achievement_sum = achievement_sum + creative_achievement
    n = n + 1
  end do

  close(unit)
  print *, 'Fortran summary utility'
  print *, 'mean openness:', openness_sum / n
  print *, 'mean creative achievement:', achievement_sum / n
end program personality_creativity_summary
