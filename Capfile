set :user, "watcher"
set :password, "watcher654"

role :fe_rj,  "riols84.globoi.com", "riols85.globoi.com", "riols86.globoi.com", "riols87.globoi.com",
              "riols88.globoi.com", "riols89.globoi.com", "riols90.globoi.com", "riols91.globoi.com",
              "riols92.globoi.com", "riols93.globoi.com", "riols94.globoi.com", "riols95.globoi.com",
              "riols96.globoi.com", "riols97.globoi.com", "riols98.globoi.com", "riols99.globoi.com",
              "riols100.globoi.com", "riols101.globoi.com", "riols102.globoi.com", "riols103.globoi.com",
              "riols104.globoi.com"

#role :fe_sp,  "spols01.globoi.com", "spols02.globoi.com", "spols03.globoi.com", "spols04.globoi.com",
#              "spols05.globoi.com", "spols06.globoi.com", "spols07.globoi.com", "spols08.globoi.com"
#              "spols09.globoi.com"

role :peleteiro, "10.2.121.200"

task :logs do
  # cat /opt/logs/flashvideo/httpd/flashvideo_201102*_access.log | sed -n '/EF_BBB_T_/{ s/^.*\[\(.*\)\].*EF_BBB_T_\([0-9]*\)_.*__utma=\([^\;]*\)\;.*$/\1\t\2\t\3/; p }'
  cmd = [ 'cat /opt/logs/flashvideo/httpd/flashvideo_201103*_access.log',
          'grep -v "^$"',
          'grep __utma',
          'grep EF_BBB_T',
          'sed -n \'/EF_BBB_T/{ s/^.*\[\(.*\)\].*EF_BBB_T_\([0-9]*\)_.*__utma=\([^\;]*\)\;.*$/\1\t\2\t\3/; p }\'']          

  stream cmd.join( " | ")  
end

task :run, :roles => :peleteiro do
  upload("../gvrecn", "#{}/gvrecn", :via => :scp, :recursive => true)
end