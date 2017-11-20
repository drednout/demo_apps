done = function(summary, latency, requests)
   io.stderr:write("uri ; rps ; latency in ms(50%) ; latency in ms(95%)\n")
   io.stderr:write(string.format("%s; ", wrk.path))
   io.stderr:write(string.format("%s; ", summary.requests / summary.duration * 1000000 ))
   for _, p in pairs({50, 95}) do
      n = latency:percentile(p)
      io.stderr:write(string.format("%f; ", n / 1000.0))
   end
   io.stderr:write("\n")
end
