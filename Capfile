set :user, "farofus"
set :password, "sobe#tudo"

role :peleteiro, "10.2.121.200"

task :copy_and_run, :roles => :peleteiro do
  #run("rm -rf /home/farofus/gvrecn; mkdir -p /home/farofus/gvrecn/data/movielens")
  #upload("../gvrecn/data/movielens/100k", "/home/farofus/gvrecn/data/movielens/100k")
  run("rm -rf /home/farofus/gvrecn/poc")
  upload("../gvrecn/poc", "/home/farofus/gvrecn/poc")
  run "cd /home/farofus/gvrecn/poc/; python poc_movielens_rsvd.py" do |ch, stream, data|
    logger.debug "#{data}"
    # if data =~ /RMSE/
    #   logger.debug "#{data}"
    # end
  end
end