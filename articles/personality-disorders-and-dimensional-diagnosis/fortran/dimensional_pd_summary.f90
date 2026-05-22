program dimensional_pd_summary
  implicit none

  character(len=4096) :: line
  character(len=256) :: field
  integer :: unit, ios, n, pos, next_pos, col
  real :: severity, severity_sum

  severity_sum = 0.0
  n = 0

  open(newunit=unit, file="../data/synthetic_personality_disorders_dimensional_diagnosis.csv", status="old", action="read", iostat=ios)
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
    severity = 0.0

    do
      next_pos = index(line(pos:), ",")
      if (next_pos == 0) then
        field = adjustl(line(pos:))
      else
        field = adjustl(line(pos:pos+next_pos-2))
      end if

      if (col == 19) read(field, *) severity

      if (next_pos == 0) exit
      pos = pos + next_pos
      col = col + 1
    end do

    severity_sum = severity_sum + severity
    n = n + 1
  end do

  close(unit)

  open(newunit=unit, file="../outputs/fortran_dimensional_pd_summary.txt", status="replace", action="write")
  write(unit, '(A,I0)') "n=", n
  write(unit, '(A,F8.4)') "pd_severity_mean=", severity_sum / real(n)
  close(unit)

  print *, "Wrote Fortran output: ../outputs/fortran_dimensional_pd_summary.txt"
end program dimensional_pd_summary
