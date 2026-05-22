program political_summary
  implicit none

  character(len=4096) :: line
  character(len=256) :: field
  integer :: unit, ios, n, pos, next_pos, col
  real :: participation, participation_sum

  participation_sum = 0.0
  n = 0

  open(newunit=unit, file="../data/synthetic_personality_political_behavior.csv", status="old", action="read", iostat=ios)
  if (ios /= 0) then
    print *, "Could not open data file"
    stop 1
  end if

  read(unit, '(A)', iostat=ios) line

  do
    read(unit, '(A)', iostat=ios) line
    if (ios /= 0) exit

    pos = 1
    col = 1
    participation = 0.0

    do
      next_pos = index(line(pos:), ",")
      if (next_pos == 0) then
        field = adjustl(line(pos:))
      else
        field = adjustl(line(pos:pos+next_pos-2))
      end if

      if (col == 16) read(field, *) participation

      if (next_pos == 0) exit
      pos = pos + next_pos
      col = col + 1
    end do

    participation_sum = participation_sum + participation
    n = n + 1
  end do

  close(unit)

  open(newunit=unit, file="../outputs/fortran_political_summary.txt", status="replace", action="write")
  write(unit, '(A,I0)') "n=", n
  write(unit, '(A,F8.4)') "political_participation_mean=", participation_sum / real(n)
  close(unit)

  print *, "Wrote Fortran output: ../outputs/fortran_political_summary.txt"
end program political_summary
