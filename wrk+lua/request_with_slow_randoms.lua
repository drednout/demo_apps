BASE_TIMEOUT = 1
env_timeout = os.getenv("BASE_TIMEOUT")
if env_timeout ~= nil then
    BASE_TIMEOUT = tonumber(env_timeout)
end

VERBOSITY = os.getenv("VERBOSITY")
if (VERBOSITY == "1") or (VERBOSITY == "2") then
   VERBOSITY = tonumber(VERBOSITY)
else
   VERBOSITY = 0
end

function log_info(output)
   if VERBOSITY >= 1 then
      print(output)
   end
end

function log_debug(output)
   if VERBOSITY >= 2 then
      print(output)
   end
end

COUNTER = 0

request = function()
    if (COUNTER % 5000) == 0 then
       log_info(string.format("[%s] COUNTER: %d",
                              os.date("%X"), COUNTER))
    end

    wrk.headers["Content-Type"] = "text/plain"

    wrk.method = "GET"
    timeout = BASE_TIMEOUT * math.random(0, 100) / 100.0

    wrk.body = body
    target_url = string.format("/slow_resp?timeout=%s", timeout)
    log_debug(string.format('DEBUG: target_url is %s', target_url))
    COUNTER = COUNTER + 1
    return wrk.format(nil, target_url)
end

