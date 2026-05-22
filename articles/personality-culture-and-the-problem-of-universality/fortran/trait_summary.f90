program trait_summary
  implicit none

  character(len=4096) :: line
  character(len=256) :: field
  integer :: unit, ios, n, pos, next_pos, col
  real :: openness, openness_sum

  openness_sum = 0.0
  n = 0

  open(newunit=unit, file="../data/synthetic_personality_culture_universality.csv", status="old", action="read", iostat=ios)
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
    openness = 0.0

    do
      next_pos = index(line(pos:), ",")
      if (next_pos == 0) then
        field = adjustl(line(pos:))
      else
        field = adjustl(line(pos:pos+next_pos-2))
      end if

      if (col == 3) read(field, *) openness

      if (next_pos == 0) exit
      pos = pos + next_pos
      col = col + 1
    end do

    openness_sum = openness_sum + openness
    n = n + 1
  end do

  close(unit)

  open(newunit=unit, file="../outputs/fortran_trait_summary.txt", status="replace", action="write")
  write(unit, '(A,I0)') "n=", n
  write(unit, '(A,F8.4)') "openness_mean=", openness_sum / real(n)
  close(unit)

  print *, "Wrote Fortran output: ../outputs/fortran_trait_summary.txt"
end program trait_summary
