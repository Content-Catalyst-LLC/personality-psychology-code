program personality_creativity_summary
  implicit none

  character(len=1024) :: line
  character(len=24) :: participant_id, domain
  integer :: ios, n
  real :: openness, intellect, conscientiousness, extraversion
  real :: agreeableness, neuroticism, persistence, social_support
  real :: divergent_thinking, creative_achievement, everyday_creativity
  real :: openness_sum, divergent_sum, achievement_sum

  n = 0
  openness_sum = 0.0
  divergent_sum = 0.0
  achievement_sum = 0.0

  open(unit=10, file="data/synthetic_personality_creativity.csv", status="old", action="read", iostat=ios)
  if (ios /= 0) then
    print *, "Could not open data/synthetic_personality_creativity.csv"
    stop 1
  end if

  read(10, '(A)', iostat=ios) line

  do
    read(10, *, iostat=ios) participant_id, domain, openness, intellect, conscientiousness, &
      extraversion, agreeableness, neuroticism, persistence, social_support, &
      divergent_thinking, creative_achievement, everyday_creativity

    if (ios /= 0) exit

    openness_sum = openness_sum + openness
    divergent_sum = divergent_sum + divergent_thinking
    achievement_sum = achievement_sum + creative_achievement
    n = n + 1
  end do

  close(10)

  if (n == 0) then
    print *, "No data rows found."
    stop 1
  end if

  print '(A, I0)', "Rows: ", n
  print '(A, F6.2)', "Mean openness: ", openness_sum / n
  print '(A, F6.2)', "Mean divergent thinking: ", divergent_sum / n
  print '(A, F6.2)', "Mean creative achievement: ", achievement_sum / n
end program personality_creativity_summary
