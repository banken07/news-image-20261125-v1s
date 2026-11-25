#!/usr/bin/env python3
"""news-image-20261125 v1 — "The Wednesday Globe".
One image summing up Wednesday 25 November 2026's world news.
Pure stdlib. Renders its own glyphs from Liberation Serif outlines
(GLYPH_BLOB, regenerated this session from the system TTFs) and encodes
its own PNG. Writes exactly one file: entry.png in MAKEFUN_OUTPUT_DIR
(fallback /output). Deterministic: same bytes every run.
"""
import base64
import math
import os
import struct
import zlib

GLYPH_BLOB = [
    "eNrtvVmOJUeSJfp9ay3ugM4D4o9L6PX44lvPIGrXg85MZvE9VKPRIECXsGuDjqIyn//1quXVc3mlD/73+q//9ar1NVZ5lbw/Psv+",
    "aCN/5NryC8QuH/kXiFY/0q96/olbDtUSqfyrrOVreAFvA8EHQWRdWvuj5OonQeXztuxr/CTu+ypVH8dX2w6yrvlRF7+2qyi0u71W",
    "Ha9c5sca6WMm3Y/uxYNx7ZCj6bb8q88q6guPxidKC7KM4jvz6RspfK2/cirtVecZt7304AtEx6O/QLWCXs8S1Dhd4Bdb599Rqn+p",
    "OahSB3/Lp+f4W06Tfc98CH2jnHE2db62ataPl9gVv9XUg1rPaK5+yZz8+8REidr357XvmK3TXv2O3j2UPrjOd0TNttSur3ruUQvH",
    "mU9RM6Vo4plxUhjPofHE8sl9fGyugVVf7TT6syT2qJ3f1lkgWBzljNOvc3fnt9dHnSByb0Gda3mlWHZ1e8EOPIeXDo3DITDtv+rA",
    "b3h7ObfM3PGdfdbRxJLM9XTufOpQ6TSuF1M5ZfSJZO54umYOcvJXzoPN30F3MPujfiPr6S3GfoDEY2ueVlfuCZKJA43hNTknvrYX",
    "h/qQhWMxyrmhsAd8b5nFn+Bs/hqneXPEPGIW0i+Mci/ZFPZVJlUyOoiXf1a/7xMNNMUWc2JIfs0zkbUmLpzDG840n+bsM/Vt+Om+",
    "4+kBYmDP4c2Tm75jq5/ZPcOIFohMGs2z5ArmAo1bo3lYFzqrUUWXvbZLx518PGOvYV3NV55pvCYY1Hn5qBjnUV6NLIvrqgZ1xmzx",
    "V25A8BXSX/MM0eYggsK2TVy8oLBlk6+dj6xswvcnvQP3z3h17yOu4n05n6+mrz66HwJ1OjDZ1/MAeKo+SBJbusXVgoHI6neJF4DC",
    "xkrc/GOPaO+OidM1fGhhZ3xxXCoW0y+SGCus+jQ1bL9Oe+LqBu8Y1ZQeAtU572z4zNo058/kQj4XS1zF+3vhV9EUfxVk29zd9fwZ",
    "3LBsAEjMzZkiX82HHfU0gvQbQObFnVnOsLbbg8YOYAJ0jcvmbG2uj/XKfdfXXFoDMTeHlZ+vJm5TkQljvA8HXhsju8DGEld6Px1u",
    "i2xg7o86yBHy2aSdc5zRqKlRTGfVzd6CXIlX22naG+kbKjasHivnDc0vOyNf1lCP8sfkd9HqXoPSUsYW1ncyuoV+nDNBqy5rxZ8V",
    "MHvsgjJ9Da8k0zuEmdP6aJ1zdxjUGS1vsrHxsnY26mzcCGcg1uLZf6gzGMkXs8/1tmPdDx7s3A1kbLrKgcY8p6+RiljFOtybPHuf",
    "FURW/qud1g3wwMO0sVKy29PmNFUvHymFbWxkPOmrgYGmjYaB3FzQHed6plRwlvHiIpnYwplnDBZweiP5NMmybl9Anp1bRlzll/KZ",
    "KK6yfQ64/Tr/gvxQsKogLmAaLWT4EjdvDnkjZJTzhpYolZ1vf7azfwa4cSv5hQfbbn5FqViQ9czV58Ry7elQEA5OKzOYeaccAhJv",
    "weF/1n3lCObDOj7Z9PMRcdJD6N04ByuX3zaXPh3kicVzMlrjd+daMfx8tPBeHGxnIZJhnWbOrmE5Q4BODTenQ0pEp8Zt37iNznNH",
    "V+phHp+TPT3CSandlNoKih84jL3EVykNqC3jNnDcVhdezDpdVvQQ7VG3QentoEofvvFzZQsMn2gU+1QkyByGcTp0FlHRJPPCeXEn",
    "i8XIpMW1vEOIYI+1BjgSJluPGxb2S0mcELw1DQoRp12br8XFxdMQd4p14PGdu9/ZvfJHUOfrOy83afI4QzsXt14rS29Gt+oLxwz6",
    "9lEStkHnwTNf43R8UPbH//kb98FD6Vc8+VCTEiB+fSi8zq95I/U7v/dG8ia0q1F/AfvGWqzYBDm/KrcF5YKzA3xSNhxgZmy8m5zt",
    "s9RFPkXpspB7HdLM61AUyvi0hE9ISeTw4PVkyTwefAkSqG467cCDVHCyT21dQ6NwL9dL5x447KydE22cRdH7jn+eBg78G0OhX0zx",
    "Rzw92H2Ip9C66sRn6wt/t3SFaV0tXb2sj9DVUvM1PN9Czt0Sf3roaoc/i3/jSetqaYb+dj7A+9CY+eqHy+lsORQFWq57HTHxt80s",
    "WReizjaJ55e2js/i3eIoPoT4/aYQwoMrDb+t7PYcXJUzcgjdj6MsJfYau1enTM8tzp5ZriTGryX06WtCFdDzh9oUSsaZRnN2fNr8",
    "vs7L76Emcp+K1POg1KR6mtK3n9Y0Vl/BRyj5Ywi2uceCPr4TB+pwSCi1iYw466AHIZ003b/8oZ3NwVsbN+ikKLHAtecMMlcpvp1v",
    "5z6bJk8bOGenDZtNoDrTxwuEWhB/ctMhewRH6gb4YOP+gjQ8xGyPnLl0DbJn4pommTksHTMETQVndAulRaIurxbwx6KFCP4oCaBg",
    "YMiBtFDfSClONU9pVn6v5JgxWlxdi6NTg1TLQK7dqJicNbR1uC0LptCUa5F54KgtTUJ35pY/I5JNYQizhzBWcvMgNsgm5NW4tJoH",
    "Ruu3jR1rem5fO+LGR5EQ+gFhXpxaFGwDOXMSziG3e0j5lLXOYuDxMHLSlQnJI01TdZL9Harz2jhy0mg8AM86GdSqob0PrlVQU9aC",
    "CfmUywdCAcdynLYt92XFYUWSWtiRr+50olme5AaW6UnGovQkc595kt9mdn8jNclk3FWaPbaj57tfpXqt+sw3zqwSVxcFiXn2wSw6",
    "4GExIks4LRo81jFF4BXYl92neuOe0Om8XuuMbaHGBSp5U8df/dLSQ+BAxcjQuLL82BvZeBLh9Q/Fh7/wvpzZ61FrkPl0VXfid1Jo",
    "azUPyftt9cGCd1b3XLL0TFLu5A4KspPX5p6ez3+xNs/wSWTAUajFCY1QixM8JocYvqtV4N8XZ35bnDI6YHHSuMfFmYN3DJpUoN7I",
    "dIHeTp66FQonr5XzhBgvNslDhf2qfScpFPKMfyMnRW+cCRwgjGd7TFMYThttXiAoBP8C5a3VSxxQEMJ/06xgpqI8eYgh5efsnEnp",
    "BJsmS6FqOVYtpTTrYJQOvZZxQ5HhKz8aSQ9y4gAolP8mmLRY1QB71Ibje70Ng+1iG+aPLf1tQnGflhVX4iRQ4a3cItPX0PEBJfir",
    "n52uY20mH2unX4VqEyiaP0j1gc01Dv+ZHDJaqKj8NkiDSTrc2YRdiweHYzH37ZKZuo2vYPhJIirWt06F0u6p8JCa9bgzyEJVHcpi",
    "MjvhQNKkogWBQSeJr46/EE/SldBB7hTnx6TBED2aWXa3s9rHtrDRdjIlWYTv4zxA5/hdypnrTciR7IJjiUcQ5MaZaC3r/lQp8Xns",
    "zc3JkpwqeyVIig5ndZafBKN0DVfsXgZHPIJRNBZUJ+ccDZ0abuyg4gBLra6VvmTrIaVnQWUxhDn+JBTtEIrOi3Dqfs1yh3fK2MXP",
    "YnWGPLZCHmupXHlsU4sYQeoNINcMhXFSVsfzMrmMknwNX1owJ2Dep+Z9DM+79iT+vWuxHpmpeZf9HEM4/7x1yxVG+HAqQQ6KZ6Cg",
    "kUI3vbJAXsFvew9+S/+Jp6/I6HV4lCiemUnjmz+kJ5+RFL89T0lXnM38FsuOx/2EMsWtPs4q6VUcaJCCALt9DUZx+mS6zm1+s5tM",
    "JHdZvjg1xDNRT8NgjKsjdl+D7DA4a6DEd8yiZB3oi+pEHvIytdO8Pc4phr+a7GrdpoYeA+OCdZuaQ7cZxboNhHnqNliGFilL6DZU",
    "HCk61hp+KHA7DNIXqNWSPzrZVtwHj4lNGhJZavG1zAMkKD1LSvz1tG6TD+JZ+jrYC13j15ZZ3dYggBFge7dzSMYo/A+06Avfp2IN",
    "woo1Tzq5SaKZcomEao1ZsWoNUqo1qCbOAEcC2T6etOGLVh2qGClsYVKtcaZYtR4rVGvOI1uaaSPh2I302CxgibPNYvI8P+dLD1uE",
    "RJf0pjCRTnQkYXuNleJqWfvesKSEn+m434Hzgz9uerQ6zOIjHmg6kOI2Uvz5Kx6JO1eN3x+KP+NzJT7XolszuuUrsPq6pfss5Wh+",
    "iz6RvF2dzwhMDQu+Us/B5oV39hEPRXA9+E2ku9dxKSgKFCypHuTwbUG+1gmxZlBnOuUPhOODJ1R/5JKWcsglbL3lEkgHRZImfkt9",
    "h8/tjbRO8Kh4LeWrCLj1EJ50nMTVRbs2FMNBk2fPyW4dCqmQz796TWIcIFp4qMVdWg7PN8z1wYXC873C873C8w2ebO6Sw/PdRvI1",
    "fIAcBxMAK8DCIjryNiXiKe/Uud7wLarycLJAvKQInxNcWZUbGr4yPcZD1VeLlM3QLPktUnZ6HWrQaYfJzZk+Fgp9dejOaRo7kt50",
    "XWfTUitBT9tsKe/xasdJJa8SxGz69M7r+kfR0sNo6NqhJLmDyjwrD3m2eqLgBhsgzSwTUne3esC3jOIX02jKExkUfWSkdOQNSBuT",
    "shn0INr7ob9qkZ5uNJpMceDOZuvp0UnTJaFt6waM505cg2BwdYqEC0JDmzHfNV1SGw1kpqv2HOXDSyMXaHb0pJy2x4I5TC8flYqj",
    "MLo8qSalh5M8u4qjTOFWApCcqZKLyETslxg2nSRxNo5voRTaze0yxwHb51ODCI31s9IBtoIkE6lxORfGghR55894nycr+BrUdbu2",
    "oJvIzbKHKEiz3Ro4eFSjBx1U5ZiSb41krTAPqTnD16h1FXUVEz9lexmHM7a5X4UaeRM/KAxfkYFsRGRF/OnBWVYK87PMYitfMmOH",
    "iY3ilXoEFNu05/2rX9IMg91ZBo3eKKiKoqBn4ccvaqj2A0DkosYDhk0KfTnbv57/neXyiVuHfQm7r2BiJBXesOgWJk+VT4pWHB41",
    "DzlbhGOIgvttcq3iTQsM94tslSaVXyQ7vdvrbJnBI1jssvmND7Vl0oV0wc21PsiiIDkssQ9sAbp+u0NhtgYM4oeCNdhwucl3+Lv7",
    "E7Yzr2NkR7SOnaKZLl3TsvSQ3gwkIAeZTco3ziiHbYSVj2MrjYZk1THKEaeusjfnAKJz5WRQ25LhekxN05IlOheboF5ztrB5t1Dg",
    "zk2Vws1qlkFonU05nIY6p8Ts+3CMja9Kq/f+I79Iuain86Hh3Qo5gEyAx9JiLMGUgXyEDA/tLGT409E9mynr34iwGuKpZ6fINQr2",
    "yeXuK2drn1dn+aex0voSR4QDmSRGJMhGlwRlGhtGMIRLuxYrHWOwHVHFl1h+ASl5lCZbr/TU/mKly193lvZilw9HWdowXVfUPvT8",
    "C4E/XlbnDN13XbEZOIZMD7nbQVYddgkGn+b3fzavYC/t/8YKx1Acqev04qUX5BZxbP/hVpGv8Z1OXImb2rBILg76Qld/RhSz8zPv",
    "kEnpjJ6olSctqbJDPVSb3b+KwhNDPmHwi0uRXwzMarIBRFs4ybvJhi8sHCm9ZySCrOltjM+YTYj6dXvMoucvfo5KMSix92YeDYKW",
    "lRJ//qeHd+w4dEyd833x9IFv4aEadTf8agpPJDlvZtY+ClbUsuX2DCP71D46q506/c7XqvRXjKr8mVHR+V/nD4zq9Ls8nAoLt2yx",
    "0bYV0WU56dLvKhd5kk6aXX/iVDV951T5B05FgxAiJL9zqnE5FYS7h2dZ+IRrnOttUxwoQYmHYgzfySqB4IxGtxt2lsu9OObPlv3v",
    "HHIMlnsj9bsWy4jFPGt/3OKP/lpsVq7x2HoiS27DLq1byJL9JGnLOXmHnJPVEbwr/lrOCW+jnPKtx1K+1EruRq8mvGMVZozjRmoW",
    "92td3qXZYtmwY2W2+KOhbMNDyQBI2SRbdGheO3+8OUgPZV1+CA1pr7nnq8lcT0MgmyLlo4SfqdggfA+KuDNI3cB9qMdAthpUoQux",
    "w4A4I0aH2wz2sgg/DLsvWIQiNT6Ko8V2UJV2TXp/1gcdBhC7ZW2FwW04pleBrlSrvEj7t0Xal0/Y2p8VQtqrghGmMbQQ2K1u1lgf",
    "sO3WoNI7Xx4IO5yxanut3zhwHjG34x+clH9vm4yq1TnuMtn1dpFkHLtzfDt2i4fH0V0/vJocYTAm3A55iRWJbghLX4hPl8p3Xhhk",
    "Tv+k3+MGxaPVR/RcJVo9I1gfAUDyZeiQq3Rk9GpSmzLmof+zeWhvXpXTdTmmMgNDvKqiWZf2Cuu08YjvgNa6mqGpkXIw43wI/VZ3",
    "8CkKaewbxmN9W+S1hBj5MMcNmcQLYD5neNx76WCOIz3McTjagvGvMa6Fk/3/57iy+fQTo4v7+xFft494noUynuEslO89hUOl2kG3",
    "h+NOqCLoLpJ6lOSWyjOuaoCn4ximu+U5hnHrF0QEPr4eBYZydL/7IOQCNldBOaT9WZBVhhJoiRZLanidW0lvYolj7dZ3qa9bZ1hg",
    "jFJuqRzzW/NRjqHm/YUEpiB38NOsSJVJKvFNiAlNX+RoZXzjaDVkyvqPZMr+LlL2R70Fvdu41lq6whcCwspwEC9bhCF5k/8Y/xjh",
    "L14d6a6O+bdWR39WR/p9dcwfV8d3dRKx0lod6V+sjvwvVkeK1YEI0KS46VrDoCTbK0PoP3PEjOMYrQpnG6axqRs2jO4XzbgMhoA+",
    "ZiyPW5IkpDFUNHdcT3TSLQbIPkGDSKpQjsRc88/LN3+TqrOWb7nWHXpb66O09Hvg2CYVC6z8owU2HvFl7fSYTxSrcem9apzmi/xh",
    "r2bTz6K7UEJ9XsGBR8iD1XxRtmD6Rrs687XpYdrXhEtby1zl7srd/2pXTklW2RTCGwajJvAmGhIxmlXMANYPDjqtIVR9Kuzb2RGP",
    "prD+NGSTAcEMS8Fut9F4RDy4DA4NYa/NlHJdQLWkXiB3gaFQpz8KcECkyqDZtiEarssnDVcLzVEID5DNHolaJZsK/3yVRycCLP8c",
    "DdLL41Iu4fwg6XQhPGYSVyNdKP0UAtJHXKVlSckdJJWQI5JdrfB6kyPieFrymRwp1Obco0/NoXUivxr2CHKtZP6D83DVIJVvpHki",
    "SwktFKN3g0VbCMUIwc1OEGHaFya9SWgT3y3ZJ4BNczTR6SguXqsgmCckX5XJogXXlbQCpb1fh1lRRMM7ZRYdn7t0WB2p7ZrmWVOv",
    "mnm4CrnFtplQmQayGCob6CFlQK5WeUBIdVoW5K2y5Agcf8mvEFLOfqScN7XvCTIXfaWc9iblNKV9imRChuyf4mptxtysOJThuS1c",
    "xaAwZ1neXIvL9VG97mH3tKo/bW3pqqIgG9V3ULs4VJamETDeXa5XZV5fS7McCMcZvQBwUSD3rscYBSXF5RkBuhys7iBbTKmMiKFT",
    "1Plsjz74qIM/HN0knai17hAw021K/t9XGZGlyC0gHYL9OoL90U9eRd/fZYe6hk2iJlWeXBS8kVC3Q6nSNebq1QhVj7bfpt/m5vaN",
    "dMvznQemhjFCZG8Gk81g8EHXs5p1Rx77WUdMMnXf3hJOb18u7XtWLo9avizIK1eWK0o722J/CxtEs1HCSbXNOx4cxQa//TGWorEf",
    "ST49n31LCh7lG+klucv7wlhO9Vr3pKVb0Fst9zddun2nY6ulO/0L+Q3K9SnwjkmvbiX0ah+iDL3w37C7WFtCdBki8zhk+655DFkJ",
    "cRiB5gzNWWFeOc/n+ybpWFB54q/toz0GsNMz8u/3wE7fSA/fY0hBIuqQ7T+PZ/iexEaSsTefbGzRMXwrPatkJ/H/TQNEtuke/9zN",
    "NlKzeA6SSBk55ALlkqjd2dQRMjjSNzJE8lm/037d2XH0c+G4V3htsQuMcTRphFtb8bDnAjI1LGI9pBP21BX0TdlRmSGlCNyC4oX0",
    "qHsFanO5mVf+OcjKG5SOXKvJT7mFBrNByrykfae7/JTBkSJbQyFtkbfhMyAoPH5tenyjohlOg+MCLXP+LrK03RombKuNtNzFne5N",
    "vMbk09j2QiQU0l6WE9cpPve7bmietWXi/KxoCCTGimIeqASjfC/6dfyAw0wh1n/ygITucf5V3i79IpnNVfz7pXkLXjU0l4y7hF21",
    "cLLaCwkTvGIubZmIkX5cgFLiSPIhzrjJ7HZOhupMCUpwwDBCDPnEkmIRAkqhFLLZovMRlKJ+RIXnppuI+gSy5tmZ1nac95A3HZga",
    "4hnSM4evVCVBte6cTAiQvRXL2IzOOCzisCWGknXmWgxTk6JgR8YLdSyc6PT3cd/qGgydq0aE7pTFaaU3aktYa0U9/8KbmWv3Cz54",
    "uaWw5BpjHWDWrVJaEbhPGyoouqOQWq5subZ1peMIKFJaMI+KmNpOX0pPeDAX/xhUDhQ0Oxh0Cz1sDUX4Nmd7NvDbkZzfuJTWgLg7",
    "bRdSLn7hcNvmZPrmqgZ4P4M8vnKNfJ5f2LzUzO8mqgxrfMikwSWpXNodbj2Y1ra9v9tZhsgD0TV0UfmRimeODC1lcmAuIop5XStO",
    "eRMYLcxPBhRiALfWse5ecAeO/sJfSoFzI+nMlQ785tp/iI+mYA9i0iUNvudORELjOd6rrz1FLUDJGDURFiCKmfTLo6zFB1OLFiQi",
    "mb0ge3wWVOGbMcQ8BagfkafVpSvoEw+D0+ujWDmuXMoPHYhcOCzTYM+F/QI92O7VlGbI6rNZt0QojvubIjV05LiGt1JPZPDTZqAu",
    "Q/0zXXIz35XDbEOtHZLNGQf1nZzh8+SeBsHWMTA/f8FlodYx5mtmp+poWI60qXMTe71FOxh8B0pJqAOaG3VG3r+qX8ZrHL7MVWNV",
    "BJOFVQNWRN7KI75JyxsSUxPzt7KKSTRPSe85TvHu1jCuitoaLPoqyIH8O66u7hIkfa27zEuEbK9w7qzkHAhEN3F9kEspOHB4SvCD",
    "psmtx/0Q2npcY0++cJ854bycEFG9Cp49VJfkhgClSzmDeXr5csiK8q7B3hmCfQTNF4tGKE2uPsROUVBCFtWi8MkUZMmqTWEZHVty",
    "W1x3WngrtovkxqklWfKKVCaRtBH51O5PqmYakZHQqDm6lAbV5BRkIucByfB6xpY+lLrCWjOXmsuJ0z6JHMY14k+LTs/lPVqfHCD0",
    "iDUwjuj8QsygRFpQbSm3BQoTZ/a8WeHQiEvWtXoNSMxt3KqaVFy6gopCj7oKOuypvSggrS7/igZILz/E544aHJ+FcUTIAv+s9HiD",
    "b31qElixxbr52nEVXaos3cGVnCUBSIxJlH8/e+QNc97RZEXW01yRg6LYhj5FxBxKwQz/arH/UFP+zzwukype/Vg6uoZwg80JRt81",
    "lxuWgUSjoOxc5FcITl2jefwZ3/4FreozK0KFpQLIJ7vjt+CxU/wWUrqHR/+zyZOKJ2mWIamQU5Hrum21CjmaWpsDMRO6yg8yk+gL",
    "ByLXJ1lKZdUQiDl0CzmnrToddlL4gJ9Y4fiNKZUMK941QvSP9qTEinL1KFBdOeWowbOzN7hT1orSFacOlFpuwSKQO0uS2x5AbiCa",
    "7JAm4omowZowfmZNyJ9UnMZCbPn6fhTMOAqmvV7l/uUPjLlNJpxmDW7POg3iwlQbe1xDWxmJSWomx2YrwqBb+c/xp3VrbXIcUH3j",
    "eixXEiqPKFSiBARHrVP7gfQi3QXG46oEZKksIJlLxU0tfwNkUWmevwqLGNTIsfC9ImUpIWmn/c3n4xtk1635Bqrra7j3qx4di91h",
    "AHo34QAB/xHLSp4GEEujfM7EKEWkjYS3kWKfB/v8ybg7GHq2QxdJuN8k1W/WZlC/V7/9bun2WyGt9ZLqN0n12+lT8Qb3u+zbb35N",
    "/cY5Wm8ZB1U3QUYLmwo2F3VCsJV1TT3hmUJSucSfyFYRmRHATHMId61s6Kbw64yLhYH1NQW5VUxsxsCOGNjgUGjkM7DOGqvyTZbm",
    "PYh4YFt4t6t1wKGvV4Eytxv1jdKvkBqXqnqxmgAtJsjbtvXQxxmp5Lj/+KuthxMtfdeBkPWr1jfrga35RSC++6/1fkjWyYQ3V72i",
    "Yr2SIl74trmUzcWNau33jMYwL8AVLeyyftrQYMRe2Dm+yTTZOUz5m2O+f3OruJN2CfwyEA3JT8jxEOK+nYR6j55ag+OlkJnBfTYT",
    "NMCRJEagKhlq49FlFjdmpFbo6YzYPF8FOWwHbcGZ0ByNZ48whywTvwj9VmZE7dEE9JBL8ac5i6RFcsXVBKZeFdR99r9P92kvDQRr",
    "xeSTbfe/YOU/rCisu/j7EzMPSu8ctbhBHUFlTb6m7WvYg0sZd2XFsvQSA/EDe2MK281bm/5Jm6PFfql5PbswW7dirCf81loA7dsC",
    "WPah/2kB9Li25o4jb+4Yp7njyKtx5Km5kGXjr0epxijVO0r12yitO0r/jcNvxp8/H34epRmjNO8o9bdRyn/KbMY4Uauf/e/UXRFr",
    "pu7dQ/euLrtiMS+HLjrLejcg5OXMYj8KI4lkJQSdSeNO4yo+/U3jHntf3Tv08aJhO6rSX5ZbGSpvxZ67rkOtOj+g5KDrELI9dD2G",
    "rsfQpX0HMb+ZpuTFbU+Px5Wd2rw9bq4tycSQlZ0iIq/gLOFjg40hIgfqtbnlj2LXzKfzvQ+VlQEJUik8EkyvhdMnZPRQlH6mIZkP",
    "fcEKqOZMlk7QytxhpcpRAxWBGLZS4SSUbQo7nnw4RT53Lhp1vMxJ+4epPXYOjjWKiK7+AhOgPkXW81DuDm5ze0mqE1S730iXjHhG",
    "gSQ9uCIZD1ym606Uf2dRmd8tKteCdPn7DxYVmzvmNXcMWw+/mztYcLZZE8npGj7oHPgPDB+5UYvnSQlFH+vWf0P1V1E7KF05PIJL",
    "hvQsSjn4ikQgg1H9nctqlnkKiH8nZ3u/hCxzlfDLaqhxLRoBKtPt2Ll1T94wMbJznVG5jnHjEJ/u4a+s7qxVVpThF7wJVhGX3Ej1",
    "1ig5AyJRUQohNn9Y/E3RoTSdas/1CzbD9Qu5QCt67MgjhPemRQU8VUyprPG7rAIww4xfVukDBM8wMw4EpTb0vhTnTqv3YWrNd41Z",
    "DaZtEtQsUf1LVMcxTtskZ3NFVQNzpHxtkxWe0KAm8xFAyRRdESqs0A5U03WkfXdoGUytTSZrHGYqbnqGHh3WIpT+4P3EvLWjP7+U",
    "kh9VNTwVPKJN5K1yl2FqgukuCJa9ovdAy4Yx3g5eZcmjS+r3zmSfoGzlQbrPpWTV4MMyGw1b/Vr47hpFKmqgkXIOqkomRQCNzVyR",
    "sHS2q3VsRUOggMFpxAueEZekBV9jpMwkAQl66go9L0qmgbVRIvCV8/uV/ddV2mjdSC5GKmnDTuHpWBfWGRnhr+f67NddsyJkI7d5",
    "p2MqNFx1JiVdh5xQHjnhTafJ3zwclArRZQxUBITEDmTdLxV90xujI4i9fyh/bYUqhK5LTWNytszfV9MaV9WKbwep37FXlr2DOYc3",
    "3EEyGsoXTUhu4+UX8GkMTXoOI26r4bWA6dfjEw2OLrT9Rvk3GGzUGVQqsFuz0p+hgOwVoZz1w+GI8DgtB1jm+AhJ97HdhUDSN1Q+",
    "5v6WFKXjPuREQG//ZJnH4RN/+QMY0liWFZrtXVOeJejBrZtQlbn4E9qJy2hXcL3tcktez3c5x2pmtclL6UfYOz1aYDqOUovxRtyY",
    "pz7HfKP49kOFZuyJP8dJJPDAaDaGx8YCLhxHNIAid5arYe8wicI2GYZS3EaXKyiWePul/GYFRcGCIFc+aimq2DfKT3xKky4MvOHV",
    "ysVGBtpYQVKmQ5TQyg5oj6UVcmYJtseC+5fycOW7uMZ08Yt1lyfKx3i4xrNT8jfSOwWngwYMLewSFnGQlhaMrqoaOsU1DAsHstDZ",
    "AvGZCWna/lpR3Rr8jPq1CBUQxeRpSo1I0l2KOsU6LlHSbSgFsDyE2jyv/RfUojmV3t8opK8QlcTk7UTdIrsSVzOLxdnHev4MSjSl",
    "OFp2qb42YkfZe4h8YS4d44ZZ9OofIy2+RIa8WAXSHmTmT5k5P6q00BVcv4bdMaT28n06dUGpxgc3Xy7xcy4sFdWrjRtJMUmyc0Qj",
    "g3TMBEtdTSV4O5JCekguVyVRkCDJVYKa1N8aK7XPEIDoJRElpRxupXgjc8JIsYIUqc/8UFlVMx3vkdg2h36gxd/Iy8Ia0q5eqPPC",
    "JcfjSREv7W7TfgND4meTuoHv6X8xpfeK5sKNKO1Gw1RGbJeQ7twNkcVJ/Oov0/k1Bnl5XFijdfao1iovE8SiHS+kY1RSR9l+iyeE",
    "pKapypxGa2e7oTwMlnkjw4R9F0WLYCBI1eUuoFViWYHUWgOl9YexMdsFJbch4sxaPNxqNaU1DqokE5+sY3uOvxkbpJbyPqUDRpj1",
    "QthHYjlm2H/GCzHcvPALNbB6Kvbmu/bKYXhjqQ5JU90pKSVyepx36Bpi1geXLpLh9L740uEAH0OOk7R45tqawtNXXmjFUcAfKBsQ",
    "Ykm6o/+GonMRCi4dDVHnSQHV29dQg2CmqOgW57q6qFxyeGdpYR5aEIm1mdlfDM8y2IplZ9R4n3u/GivIkhOA4noEeEWnSw9u0u6c",
    "1+RrrI5fLjWliyQmaqsQzdzbz84djiVda64WjRYdeeV3dzrjlP6fP/0v/OlfrJOhCC6RPSz0DttC5O87qRAvZlBHBNcqYYL7PHJO",
    "o59OUZuvILScln78dW8jxZ/1mrOWUlv3NSWhF+c1QVDDQkW0f/0ah6shEKh6Y7HwEBQYrh7qb/mWm89VrNA3UotlAO0IL5scKSQz",
    "vTPyRjoZlvn+iiRoqtmeXanmIgLte1EVeukYrcsYQo4Gg1xZlWAxBRyi/kz1Z+HGw7dXNwgII5RTCkScNILTqCpnPOCYMlmriU6z",
    "b7NpNCOZ6XtXF2vUf/J6oOiY14ySwcpuIanUo7IuOEJt5UY9pBv1oLbO6NIR97FP4SeGHlVUl+mFw0gzBMozxDKDmqG40fFOnqHB",
    "BHBX65oxQyQ1Q4PpJJyhyTqjTYk4JWYI5L4XXUMZ0jtnA/zUpgo3WMfmZi2YHU3et8XMdVaLW7otJqkW87i2c67cFpNUiwVBIRF2",
    "3xbXcVsMct+LajHlVLYOBlm1GF4uXdtusMbfYUeDC4R1jbCiFJuiurSMTRlRZ3CZ+3tBgVu5YlnxelIJ8RWgU15PeNbrCRANXk8U",
    "bbWeSGo95agO43u1ciRDcD3VtL9H0WA9fbH1ajRJNXr0aDTt77K1pmg2wnjUbAb0qNkk1Ww87WaPfJvd2202STWbpJrNe40RMm6z",
    "Z71FStXWmTwNNYnhyVmLnK5KGLEXDLs7PE6GK0sBV1bXhSsbF65sBlzZDLiyeeHKbrl7hIeKDVwIs9Zdq+sr02alhMEWFfXTjE/Q",
    "UqHv7hnQaTuqWO6oa7lT9XdhoNA3VOEqu7ZUFOTnV/xp9FufBmXpaMRX8rx16vK4heqYdO0qY1GqTknZLph5i9XxeX9/jgBq46ei",
    "+v+apTx1EFlFy5gNrx/BG34ChPivP/4ESPdHANLlqcGLoO4XAX0sHxRT+UlBaCvyOr7e4OnmLQtKd6oJxsuSKikiMmoKfDqGxv5C",
    "uTtdQwtU7lltmd4YY70VBExoOYpw1/kqxqRTMX0UFXhKLsQ1SiZGonNsACMonyyId8y2FOh1jAsmRswfF5OuzIj6wbdg22pyBAxr",
    "6iVCcpZ/gQdWFBivbAVh6mnxy3yITiUC9edNgYMW/3gJRwyuiB2s/YnxSzfThigjLUrGi5pvZb6ejJpFl0JzcNFD6YPwkopC+K7a",
    "tfd8o9j8rwZ5VKpTL/4V1e9NwdhYvBSj4HMNTLphTLoR3jmUczQsSFkSYM/dZGrnr5HoUE5MpURZiLS7LKuKL1L/V4X18WGRH8hR",
    "POQIhKUwPAiePMBlOSMRuDA7wOeKSsvH6wJ8zu2mbr6+kQE+tx/wufaAz7WLOMfq+SI7Ecum01yyNswoTx7vYIbl8CeW0qmobDAF",
    "AVFsit6BgqZy2Gfhd9Xchx9Y2GIswiZAuhG14WGrqv5GANKtC0iHWTEgXY8YS1JMHIce1qjUQq5pe/s9EopBsVMoJqRk1POksKgU",
    "Gj/mjZKX4wxxAjdiaaftQV/OMoDM25sj9p32ycfFMP8ANJ2PLmPTrcAeGxebLjIu6Cp5sOn6g023RmDTgRIOHWxGUqRVglnHWoDT",
    "sZKlTI35Vvnu9cLTMRXDh+248HTIAtNTrO2TW75JxMIcrBeLj854XW2s2N2GSb0A1NIihcZNfQ6PT80odFWFSMK8h2e/ODSGeVv9",
    "wtP1cuHp6rhXWWNz1CD9GEgj1DHqSAdYrxehDjW3fBWfMELdePDlQLbtYqaA4NrRhqHAMuDa+CqsME11pkAGxh0YC3cB8fDG7cSQ",
    "MRnZ5lO7PQuBActkCcEwR0Xw4aDoFwtwKhNNxTgZc/lrr1BmFw2lyYt5dqecncMyu5jD2XcuAYCoaKenQaV2hb51MepgZngjfUMj",
    "2J9cebRACJgOIpecTDhJDVeHtawgKPRg1KBc+shwdZlbJLnAo7T+MS5W43qKoa9bQjVw6jIdE8V4X12IKICYEHwL0D7kzkDSjXJ7",
    "Unu2dgtu1p/q92M9QHUPbKNGHpgNqB2YVAEIdnnarKDMqCYMTtrRFUbSbDOChtvGMCWkOlCyvMPSjJd8MQo+MapBpArb4uDLqsEJ",
    "+4qsvpEqNVlxIyg/TbI8nXFSb75X+fpMxfIPINWx3ngXVF1zcjAvXMDYm9fKmjey8Ndy5ZC/wqpDcQhjtLF073Rp+k8ZGJnVo5Ao",
    "5jCX/xyrrgdW3dWW0tiupp9lqvoTVh3XdGcuQ5UA51p+ic1kDWt06u9h1SlPlg5RlXxgJH5xoHVhZAAoj0MWvhnum3GwEPqs1ItV",
    "l/47WHX9L7Hq4LyKPjn6CeCd8M2pJkt+oXaF/UgQuKfMhcMUDzkZgRAMx40M3CSHf0ItlLMFCkDzbQTf87EoQaLymOn5KbmbAxs1",
    "6lYw21jZm9QmAqpKH8DFNZfvBN4UFx/KgKAga1oGqmMlawDVQfNg0gAow9Pl8kbpVzz5UFPNyuWNCnQ6Q+BFfEZ3Lcj0TvJNaJeA",
    "6sDTKlVNoDih4l1zsTBQgTXH5FIlOoarkcyweIF/ik/BKPUpMZI5CrIigLoZzZ860TBdOq4O85FEZ6OsuGhWEJ+0PiBNyfIwScnJ",
    "UJ8KtTgE0SVD1yG5AUM7kTIc/6T9nSnEv/yLKf6IpwVdZ6W88Qv19aDT5TWviqxjkbrd1AjEAAzrZHhOelot3dfwTulpBM522dEi",
    "Pa2WcfU0A9d9RhSLlEiUYY1QgfgpM6hC5bkj332rO/+HgNdBtdTzoLYcGywHqbI0rN5lp32Lq1BPth1/ObBVDyWdoNUuFQUPr/D8",
    "KCqIdX0lqFzsOlbFJqwkseuYJ5DC6TxMJAcLxF9ZiokMly4lfzuLqzrerF/0OuaDOT8qgOxOKwK9jslc26BJr13HbyleWRGQyFoW",
    "Y0R5eKlLkBRzMYbT2NX6jTDDqOkkB9bRs6YASYv7ifpsSP7jXiUyjOqjc/SLoFryurVQa/5GGs5A6fvZnrALcfZA2s2bMLJVYaAF",
    "KUg7kFtJYQg9l40X/j3J5wCTswtkOUENINjMTvmFUSOFcY0YYYc79YC06xfSDpeEiLvLn8Iry7w+nC334ZysL0bR25Tt4ZTGEB0e",
    "0CM5YruypcHCrTIukB0oVWCC32kU5d8C/qY6amLccCaBoDeWKtqueqK8qo7oud1MWbsmKRgCYvp4lhnBpVnu+c4y3a6qg9OfWU7P",
    "LJf8jfQs0yivjO+ZH+DCB8huP8CF+xYlAikxFkgALqMPJ3OKEjkQErE1A76OyRVbsMPrhXCIIj9Zt0Vo1ftXv5T1EIavU53E5cfe",
    "yOYAtfFG8eEvvG9RAAC1qY93iqgCTIBIPOPDpNDoyLks5qg7YOwSiwRkVphXuYBN+LFpKmDs9g8wdjcu8WaMQ/ZWrcxYj4Rv6JHQ",
    "pVxNMqHlvCytTKix2Ye/ViaqNApyA5Gk8qDXFUDZiLQUKmvdvobQIGFmwak9XPblnbq2r++k/R2UbS45R7i2OSoYQycCThclGLFr",
    "Ee5t7LpGVAphQvl8ahcVPIe+BYtoNTGMERZeMu4Q9bE+2HUByai893ccRtuXaFRS1rnAQZcdwd43hJQpjqwosd16kIryFzwrOO28",
    "xodFPsZDSii/I66htyMRgACByjlizJS2C76yTQmwjmh2clc5Ngm8vjtKCUh9ugbmPKTKkSqmlvdfANaxjul2fWKYfz62a+XPNypM",
    "n08d4/1U3omsD2qfZKPPcuixHPBNWy+HBZILbK8M7uwcJp8NBEKh+AGVRHFlQPXhKYFn2wrKcHX9gaubf5JrRmyuEahvYxnxDgvF",
    "cHUw+8ukTBAKfgAlNoqIANXbtkExafgnrLp15SCam+jTQv0GfxlVEmVkwqf7xarr4yJYUB2HOVh6X49nQYUI6U1OZ1iAdHvhGEXs",
    "SwBHEg4IcKTsJ9nDfhe/2iN+rTALitQbQAqrDifBHDWw6gzlNn1N+EpLC81Byd1Ydd1ZrD2w6vqF3i07/YRVV2+lVj5srLp+sepY",
    "dX5dT7LEy/4Dal25CLbTKKEQ/hXIAMOHYhFUTs9Aj6rUivxUMVjtTJlRVtTOrwpMBxQONwyRJ5V6g0oh1pG7rwEvFKr0V70AdaBG",
    "i/ICg1FljIdSpQLUbaRJg5SC6Wj8VxTUjNJR/b2glElOwZK7asjLBkPzHukFc7F9UKNeaLoVBr8VPihgmgkDE7Wj5YOq9fqgSug2",
    "tDFNU9Zt9rYPKvkLX3h0aKRHdRYCPjFlCR2qQqnPrtEsnW4l+DARTvGNzdfwiTWiAdNVgTbDpvRdfgPDsDUMQoSbH8r/wjj026Ie",
    "LUJwu1oESi3C8eIW1duifls0fK2z7naNQC6BfoByi/yNLzIMGeVyKNo1uYrTRa6bF7muhGRqXRvnq3VtONE/pUSm0LVJybwODPZk",
    "x31TkS5HQLEItbJ1YYEoEWgg1Rpfl7oNaGRdY6utbhPOjpaNs2JpR6Hhblc5XOuFszOogX+9dOrylc4Hzq4ZaEk3DEn6hLPzdxhx",
    "gR83j5NDdJf/gyEh1YCzuxR//opH4s6V4/eH4s/4XInPtejWiG75CitxqqWL8MwPnF2/5O3qeEZgaFjwlQBFtgt+pxJ4dj0A3Ga/",
    "AG62OLDWnBJmVqBn4zbvwda9LzFNugZEY903qLrNQDlelhy0LxurNciivYKCC0TbHKGOckvBZt0VGFEDZBspGVznNOLmqoUyf1JN",
    "yqOasNRlltbJM8bQD99I6yNvR0N7YIjSU3OWoZzCY8OkqqRzmz5JWf5fzhzExm5p5owfS5CEIqFv7gC0E1yuagyiLpj2JAzmxaVG",
    "5sWHW8aMQ2Gvogqzk3k9wt/NKYK+BQ63Ahwu+Q1k3Debr8gZmhKhNSVpDqGH4PxVcGliAVIVGV2NJINtclyFGV9xMZlYaqppTgOa",
    "gCyh4pU30khyOBi3q00jRd19rR+KCeZ7fRUgXNVIngjW25e0tZEpEq4pzKqaw/EnpqGk1bjMal2pRnbjkM6KVTm0AlTQRUgvn6ry",
    "ohgSFbCCAb4IgDCxQq8YXE1UNJzlBX+s+AsrxWZ5qhR9s2YU8/4JsHA8gIUlitpwYp3fPi9g4VlzyvilaYglTRyMpZlbb4CFXOEG",
    "LCRSPUNnUBS5qnI3wNqFiovHaE7ly2gnWFAJ7a+GzkTqfFUIP1yXU8UEEXYmgGwlJ3FTo1KDLgJJQy4pfJBVFrA9/gK3Dsnx1XES",
    "33HrNJzMxErOLgvgunVJCcnpItfN78h1xr5ezAG4ED4KBYNWfgufiFIRIGLXCcAzavMrHpmO0y5DfGDXVVXZqS6z+qLJXhWkSGal",
    "B7AYc832bJF05t1DTs4jYgZEoWqOy03Dnk0oLxgXVHUHlDy+cCIbuQ6GaqmRdM21m94X+TNOyGUJZ3oh7jW8r9Ad7TIN1aNJfNKU",
    "giqUKGVcXaZcVPaJ4Nm93PLr9BUS7Np0qrdQ7FZwCU81ofThRJCcAlVR64ij213yPsUAaMyFFwnXkuDrIJgruERQPH8Qvg4rLycb",
    "uWtxEZiVwxDQrrkEd1XF2B4qUHSVcmZ4Sav6uT0l/tsbhB2rCMv8WgnqPGUOuyRjZPLIkSXnyBIuF0UMDsL+dHkk4HEqpkZfLmJb",
    "WXkSB9Kq4QvnPiRbV73ocqE3MX1iZxTbkqqwn3EIEmOt3896lVvC1f25eV2tGIyL4WRRrRkdd9WOxCoAZFBEvNW5zVrQPy32nHXE",
    "L1eQZVhGUg7h8LUNWdMrpKlaNjTftzK1sfhYaNEqtekAs8OG0dJB5oLA7DDvzc5G1QyKP17x6674dVf8uCs+fMUYmW02wNizEgA1",
    "tf+rvdPvm94gUN4AZUinlC5uWNBM+lKt6lZijCeBw35kKFUyZTW1ERigoCOW3QrKVTBSC2i7WZltYTZyKbERGJNFnfFXNAMrtfDw",
    "VfNht9ZqOgMSpKs9a6TO0E0XN9aF7JjBFz7UVQbo8mrENcxqQuHs8ec/HeY3NKhMD1KKgtNBMt5Yg8wdWZr5SjDwNf9ivIX3zvwZ",
    "Uesi3EHpv1TTAYQkD1HQ8afESCDcdWoH5lbdWHRnB6YRxXKQo7QDoUNuhxLZvhArXYUU66gFV2tt/MDVbuy9uVq7Zs39FK06cgj5",
    "ebmQvtXVTVnxS3GAjDhX3AusHUE2Rr2L8Q1aUrNPm5/4Xv/O9/Lle/PyPR50CNf5je+ZEx6RjLkIqn2eA/mOaG/F1BB+FYb2jTTy",
    "Hct8JGlvQL7DbGiNdkON+J9YV6oK+Pvyy3+x/Fg+/o3U71pF7e5aFyWa6Z30DUuoZStIL+X+htzYhZIg7kd8QRdpXyMkJdziAtuu",
    "frVUl5t/DVg4Q/IiOW6tgIfSz+iJ7EgqNIlhqyxvwTJHM6DGeghXTGNVRqeFPtdDGm5VEZB6UMUDFr0at6/x7iA9nj06jabYRbCz",
    "XQTRGuagilGU++r61O7fD2gqSQ86PaGtmBQAHqgio/y81Tr644rZb9U6GODJ1AmuxY8qRBSAQpNS0OKt2J6VbLsVeoXmrEDAW5He",
    "J68kKIK9oNP927KdgTbbxhtUxnhbJtSp1SvEOndXqLiiNc2xNagUtd2TKw9RXuGS6JfyVOfg3Lm/sf9f//EBOfZ38tvWidNCZbaZ",
    "l+GrgbK+Lh0n9xzfTu5ljMb5LIbfXi7pZCrsSvwzhBdVF/bph1AtIxivh/x2+v2b7v9Z0mDI/NN0g2foZSv8LUBA/o6K5xwVk7cC",
    "xIyIoH8yIf1Bk9jIBrFG/wbAsh4Hj2hPAx24np6Z7hrDLVpjy3CYmaamIKxer2ifSPYPYxIiquEfvyPjtQcZb/wJGa+X77SbKSQG",
    "F09YPyHjJaWQ13HHdsTYWqDc8WfecAeNbX64z8N8Hmy8N9aODjTI7ujk/k04aFHPkoek4I5wSCrOME2XDQgwQR6ShhHPUcYeZIDj",
    "wTq+BIk1whPA9PJAmbj+AZ7PrEdLiULPp2tYU9q+w1bbA4DGBhsArV1AP5KOfczX36bseUUlfVfPpJWs7wLkrqGBRx4FqGyN901+",
    "S29CW30nhwIdGb47LG0OB/NnFbH9wn3Cx+PDFk9HiKfjH4mnDDD+LXGGEleVMcK0wfJAqo4R7KrdkSzrXYDkvu/Ji+T/q5miC/IX",
    "03uNH0dHghgAoSMUlkfoOadVNQbIOCxd9atUHVLOHO0+xELIM0Ab34WqG29QdW8QdmldaLvNUlry3OGoz1q66yr4sAvkdVcQfKj/",
    "c3sG02RMZS3eFulMXF4+feoVsMybQfyj5TWf5TXfDDTQ/MM4ywprI8CxjEO3YZB17PtjbtvBk5uLISuzMiosDMLi9QiYpUkoUz9f",
    "lNVsDat/tRkFi0cfIiWvUqI5yNzEuYthDFi85Eis1AMW71xRRlfeN7cLQ7NVFBt1NqajzVbA4i1FBtgfC0JOM1JK8IHRREFz0BOE",
    "/YtaaPT+w9w+VB8N9TMFyo2adzJcIwxC7j9VxKNfrK8fEfDu1T0eBDyoWIL+meEl4WBmIQcyE70/+HcqJMsCKbyKdc8Fa9KpASSZ",
    "SAGfj4tkQw5U6CxyJ4yJKR2XFjtEHawgW7LbrNwYm4ugU0MdZcS6MkWNcPcHEe4ohVEYqV6rr2oMYfzViXp3g5eJyn1e9LnSfJXs",
    "BQq8xK7q1Uxt0sRFrXqzC8j3ajT3eklK+3qVhMqqarJLJBbG/kaGoaaEvVmhZ+hp4FODO7GK8HoArIij92svUTbeFQWUgGxObunl",
    "EWbKI8y8CTCPRiQ6hJk5HmFmjguAN0e4oCDNfnJ6WEueOT/Mz8oqMgIHTzGlYliMLLd8fLOjen7E9PSNjN/X89ByqQ1QZbebwyGP",
    "8H8Ccmc9hsK7FOUc4HFgGoEoV+NnLqLxHeBrPHhKI92Xavs4NK2FY0Ygd7ZCjvyoGBcLGh2IFDih7JWUowNQ1qJNT/MSyqcKSycH",
    "uF3fAdaX253CR0cpP+Bmi4xktRYPAYmtOfGJV4uxmPal4ehtDhLsV0LNLrezLq3P3P5c2vcwfYLPYhBCMF8SzGOH1zAvwFcnF9C2",
    "1Lziz4yyUj4Is9xhKvAYCutt29Oy+ezs+RyEQi7UWLCQpA2sd4QY1O09lZ999I71TTr2VNmP1owg22vzjxOy9zghXUVspXL/8hfu",
    "XXVuObwAY7avvZ3II9ZNIRMqn3NfTSLDsW2INZexrtYDGSlJ5inUYVMGu1v/Rt/8TnoEnyUIa6YjFXK7W3qvq+aRjD3a0nc6RnCv",
    "Z6EA7A5HgSxRxerli1UzlDBzweyEdlejto0ZvxS23B1uenr8oN2l39HuZMV8o32kXM8YNW4XRKr2kZ3tzf5dg7ftmgjGU3wGmh2k",
    "NWsj3v3xjxHvbvi+pQGQn4ogEcxd+g3x7o9AvPtT6of8YG2Hh/XJ+AhY2oC9++Pvwt4lpfHMaBKNz2oo7QD978De/QHYO5hQUItP",
    "wcYpLHaIfpQDvatQSAQuu9pzPEB03eCEbwsPLxL23R+/Yd8xl4vYduczzyVj3/lp//5g3y2F3hj7bi3FpnaVlEKFjhKBqwT/URLl",
    "CpwgrluRfETdEekQ1+1oR6fjq777URFYv1zG4EC+AzXTvRZ12zkRUbd9uJA60gfmrVayDeUVVstQuce42akGvkPGOhM7KZBs4YRE",
    "zTzEzypgEXBe3cB8yQWBB82VjN1j+cTlvHFdg9BMuyqzVMaTe3cpw91VhcknCn4CvsObm71FUaQTmRFNleYQAmYpuxn4jgvxBmCq",
    "mktT3ZxYlqrwouxxzcSSlhFly1O/6HeVidA4XatlY+iFy4UEFym9VtcaqzkpN/QMhYugZ3+e4d39PspRn7qCDxTmqlNYFKBkoKyI",
    "cp28nL+RySASmcDnLsmgIl2oOCFx/YKqPSW2MTlGeJB/PgcpLDySir5aN44eauKf5P4CXGwNpDHwJFauLjQz/FWABaoLK9WgWfDs",
    "vlfZpBZQ00dh1v+MyZ9RHg4534YW2FF7uteAYBrzYl4A+Uc453AC9eI4elMFK3JakxWgA+oMLAVnw5knEHqu6+K1NBU0edalq0wC",
    "AkMmQsRy0WHfKMz0m2nVLZjp2lIJEQ4VgfOw6KLocI5EYwQxq14bWKyC8abCHxD271jl3W95uTCoLVUfJqFC7gDDUO3niwaCPkUN",
    "+KhdDhfzrlIxz/KYUoSxe5SowsgjCdvUP2T4KPf8YvLeO71dDHiIRZFSPQuKMF8o224EF2goS6wDaXfMgVofAp6q62Pftqh+RwnA",
    "EPgkHDk7RGUWZNA1vBbxMIkjnb+vSoZDvwR1UB3YogBp/DZpKWEskKyM2BFOiajvlCoxYtvu2O9S+XvesQgYqyg4lhyLQMIrZ6e7",
    "fCDCM5tDD70vUIcybwezve2LEvvCqEhTsW+ETUU8WFvVq7fdFV1v4T9Q3alM5Y2aitdlzocQHLKe5fgVCzZw9yUD7mW6aOVcfYht",
    "q18UuGF+sbMfn8Rw1twLwL1xAfcwMLqqrwhLEaRw5gZPT5GMx0oqC4rxVPI401arAPdGXCWZ5vRVY+vV+Uap/fj1oXZy+twYJlwn",
    "2H9GAC7t5A3tIF1We5UdrQlmD8UCalPFWOYKw4LonD7YkfYwbunvMA29BZODlitMuXkrx7O4vjHlxr6Ycr27gOdGWgxzVTY1q+Rr",
    "wvnDwNIOQ8WsZp1U09cqcxWK+XLRWi8onTWj+tpQhK3DuRX45nhnhz4nkZ+OK0yWI2FhQR7/aHEUqOwF7cNNBQehNetqp0G4m5It",
    "hsfHWi4f9ynp3dBalCkiW3MnFe3f9JOits66QjXJqeNokcr0wIpCLYfPLMWj07Y94qoqYoPFfFZVQSLeh6pAlRVXZZ3GnH2B16hq",
    "CQ7+loWii5qV3dTwWmwOmNYh1AzJYrwfJPHwGqwUug+Uk0NZIrO7Vje/wVXZdMwIKD2HTsKiD8pQEnJM1BhZCkFjLmkNOEqdEj1E",
    "Bz4YsgPCQQ1Fj6sug7KC87sS1zD2Bv5q9Jm9ZWJQPyHAl2ruwWjLAx8FVYXTQhQX1TZGINeu0fQoCjbGe3Ww3/Zpm24aQ/lkeslx",
    "lPVHoqoXUu+PB1KvE1JvPyOnb9bgDfYDRvDST99ckv9z1C2/xdGrOZJQj8PQNSUBoh7CiqrIZT9AYWh2c9pQexjd1c5Fph51PmWY",
    "5xukbbvspMPpDHrHPkvf+cwGq2HpWPS79/pEYDDLsTkl1e9hsJPeTp+pv9kupJ5I2bXEnq+l2n1JV2lEGa2oBs2YLvTwi6mdjHVT",
    "kqdKC7cLqQe30Fs9E2PqsSvC1COsjpbOpWiBk4Gb5Vyk/yM8ssrlv2tcZX2HvKNkQ3CKwYJQfJOmdwfeQQ8YEA7t/LYVvdS4oBq5",
    "OOFAVX6NCIjNVBTAvyX1SfpTQCqwVLudt0CztHdivTKYoyCRlxp/tROrVUoknzcZhgHCUff3HRarvfgkDJiwf7TDjKuXuMNaDEiO",
    "HdZih6nNLcUffzO6ybC2qoUT32yPyhRV6PXNrZJUYhFjClcP+ox4H1J0g/ddlKQesGrAyTIaFgow67zJ62Lo1RJ3MpbGV0GaS/Kq",
    "6kZM80JSDoRoD2EnxVq+H9SwUWetqBMEVUl8kdVcxCyZOaCrqIwxlyMCZ5QeBxlsO83LtvNl22bXtd2/WizZrQFhtp3XZdv1su1o",
    "CSXJh22v9d9m22ah/UI/BAst6dlj2VqVXoTT5+9M7v8lB9vfG6G/A5dnPeNBdHur+ZLegPNK/x04r+igqX8GzqvzG3DecLkXPcrC",
    "L7vHwFDKYcEWST7AGJXkg0gNAT7NfHXI7MQXeOB/r/Uyn1ovrM/FMSiPwUeSUNcooEzq2sUxPmEy2ddk0r+ZTOol25rXZNLkWw7z",
    "yLhgeP3BbUOUVhQF61Hjy/ZHVQpToB0RWlRboj9wsfOdqo4Z3vEQyGXrqVdCCbUHjlyJGzRtrWTTlg1asIbIDA0EJBm0UPYmRwUz",
    "pae1CFjk6I54h9XtbJ/9MlIei8wAKg/Olaaa1Yj8H9+1frBFmRW7tX7KE7EOc9lRWlbIPyOHvQZ8WBovzGvSeMFvka3wxfzAGBm0",
    "JAaMtDH4dv5G6o75DOlULap8rzL96RyQMom+WWVuVOjNKl/IApwi6K4DIRRFgoBpm5RYYyPF+bLAvOR2KdPIguzNtmkaGHoPng3W",
    "5kwveH4VVywVojtRa89ILtszxVq+1DDWzDbFkixG0whAVJZ6VC1CoFyqDMAwn6Lvbpj4iU/dU2/+Cz7V3/mUMPSGQg4MQvnC32Kc",
    "JUS/Z5cADAy99KfSVESYVKWBD9mwzoRou9YUFITS3q/TOxAiZ9iS5MBkQT0qoqxDa8rFEkEpoB2WdEmmR3j3aoNJLssu+NGldMLB",
    "JkNalDbtcSK1B1U+XWRX1rhT1aRNXqkUWlEoQLtofOm9OPGzERktBOs1o1ayrhVg2Sr+GOHiQ6LsNmgkKsgMVzndRheDZ6Er/gnp",
    "Oml5v0tjqNK5mb8DEL0HgewNz5Ax4sVUuShUK6A9L2EUvRlwa0U+IU5D+0bainMRdEGFFae/UeEAPP+fUQxAhoNuB2BWPlMS6IDW",
    "QSYlryRuay44EalTBNIDt6vgAayyI1g5QuMV25eauCbrKrJMRtfNQuNSZnBBym/xNe2QGkL+BdZuF0gMlOLqSKmYgkDNXUdKGCXc",
    "zwI5YGX2GdpFj22rT4CyWenCV5G6XnTbdqw+oNJK7NS/ANZbT9W5/bid9OHQlC6w3spvlHsNBtbCwVRzCQS6HkjNVpFu0/8ErGcV",
    "SYeZGmvfuw/lNrjCXosIiiOySmp2/EwMFCOD9TqSAWc31jvpG6pPT9egNV7fG1YrMIPmdY0m12f3rzFEcXjfs3vmN8pD1GOI4JNT",
    "qxGowK6gu4GrR2E1CQ7xxXXV39cVAt0eSj8ivijejUDZ6QhYt474Ct2U18t8p/TrujIF2YfKntMyHc6CkLxdvCvn+9duiqHCuzAH",
    "OhqlRsW900TeVJ1pEv+3qqaAP1T1bLXaiczmc2gCVi8FrF7Swm0GHmClPUtSsV7L1exTfqM8G+vbgmUoB6oOe8T23Wv7WbCpvZNe",
    "sDXWD0Ze+HYMKZJYzsCAqnKZBBKmzRzBt4EyRkuowADxu1CpIGCu7MKgQbImuYwfK7m26q9SXGY10ACNfkP0AUnhxBMcV3AtKqIY",
    "CHvU0yGwcziv0t4iqs/sbVxGlySyJtZSWooUX90FsDJrwbnI2SWMLJrfKSHsVaDdJG+vHVqASs2x5sS09Kb4jrmLayeixabqDO5W",
    "6uvMobz0SGEoRmPr+0Z1tFYCPwyOGAPsgbQsGAB7oGTUwskmfN0RYaYQqpTXhqDY69aZ92UCPwNlRLSyLtAeAZlsL9sP0F6Z38gq",
    "lIDRg+SBV2uLGupFoGL1AdqrF2ivzgCAA4aCXKD1Au3VC7SHors93qhC2qAMtFcv0B6ovcKpLFgVNI2kGvxORgQJcfb6G6peufh4",
    "P+PsPWCDII2z9wdx9jCxy9EpcIDzNXGB6FxuAQxMJgmVaSwkiJt7BaXyJMiOLUE1i6WBsYfF72EitbxcNZx4Qn46gkQa8yPFXBTl",
    "CQ7jdXrebPtye98o9zn3azWe6a4RBX3tII2wB4VR64I1XJJh1LUYCTOblwFnvWZLLGPGZ1z0d2PtEcPLhHdFHe3uFYYV3GlFTDfK",
    "SAxBucOGucZ4QTI1tntq9l3RedlC0WfGh2rjCsMPCTkMIECJJGJt/4L0p2uQ/kYuLlWtN8c3cSAOMjsazcRWGyHN9TKBmxNySe4v",
    "bEtVWx0B8AfYSDUEfvWh/GKiGwR2p67BDCVUjE1Dx7XcBkn4vaj7p6IySCVuLssn+L2jbKNUMUIHE+2RLwLsGeukkEKnVeLY1BRg",
    "THfVPGT4LhVwa9k2TaYgNlWmmlS/ROlZUmnZ7c1vnBYF/N6bp12xUv/P1f43XO1fTBUwvBzJHpVj7QuHfv5OKuiMvp4IKvsNiy/q",
    "cXSWNxZxsfjSBdG7VHc96N+w+FJg8bX9CuJi8f3r1xiLj1aJqkLaRH+AL0NRAwTK2yoSPOXVl//TFRJJFhnB0lM4gykWfux6m0iq",
    "LGuNalxCpzcEASOkVfupM19YUwDxbvraYrVFmBwN3dlXQHei1ILBpTK9Lkr1CYC+IvN6rwbo68rHmMaHZoIq5Khpl388IOgzB1HA",
    "idR7LDS526vCA0W5fq5ICU2bGGYjoOe0D5g04gohqnSw46pSD1gV1nBqDzyLqo2PgDRVAS52M3SJLQBTFq5iTc4wTFCj1pQwjFUz",
    "mS42C0nNpByUXbF7/c5kut5EYVtoJhVHMW5ai5XoHDPZGGimis3LM0kqD1dk1KyhaIxnMsfsblVugG8xusHVq37MfvsR3aUqd/vB",
    "gsYudJBuPwjfrH6QVD9EKitv3X6smp9qZNEPnghz+pr6AYgotZkJiTprRvQDjX5WZHnqXXOqjED3IqEVSTLlbNzpSc7a74rsd0X2",
    "uyIHYSSnLbIqLqE46jJuSDVX5NCK7Da8e0UifT6rCiFJrUiRO1v889qbz4pcz4pko2nG/2LSrLpCMsmWhUNNICLRk3m3Vrtbq0ZH",
    "kL2vjpR5OyJSW6vdjpR0O8JccHWEpLdWuR0pDxBgWQ9+4SwPHmasG85XAAHmaaw3JHsDUaDWcQtvzgv+lgL8LV3wtwAVQBRsFN4c",
    "t/Bmv+Bv5YK/lQv+VqLwpkEFvjgOxvrr8VkApPCzRErho6D02d3js3y2uqTijg+zwrK+TDJC67e/fW69H5/5oiiMdjvde/RaAeAG",
    "87lgCggI9LfwArcAG81X17otWOu2AKRaMNeDqWA4QCNxDFUCIDLG60eIjJ9gN/7rfwPcnJi7",
]

UPM = 2048
SS = 3  # supersample factor for glyph masks (3x render, averaged down)


def _decode_blob():
    raw = zlib.decompress(base64.b64decode("".join(GLYPH_BLOB))).decode("utf-8")
    glyphs = {}
    for line in raw.splitlines():
        if not line:
            continue
        fid, cp, adv, _bbox, contours = line.split("\t")
        cont = []
        if contours.strip():
            for c in contours.split("|"):
                pts = []
                for p in c.split(";"):
                    x, y, on = p.split(",")
                    pts.append((int(x), int(y), int(on)))
                cont.append(pts)
        glyphs[(fid, int(cp))] = (int(adv), cont)
    return glyphs


GLYPHS = _decode_blob()


def _quad(out, p0, p1, p2, depth=0):
    """Flatten one quadratic Bezier; append end point."""
    dx, dy = p2[0] - p0[0], p2[1] - p0[1]
    length = math.hypot(dx, dy) or 1.0
    dev = abs((p1[0] - p0[0]) * dy - (p1[1] - p0[1]) * dx) / length
    if dev < 0.6 or depth >= 10:
        out.append(p2)
        return
    m01 = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    m = ((m01[0] + m12[0]) / 2, (m01[1] + m12[1]) / 2)
    _quad(out, p0, m01, m, depth + 1)
    _quad(out, m, m12, p2, depth + 1)


def _flatten(pts, scale):
    """TrueType contour -> polyline in px (y down)."""
    P = [(x * scale, -y * scale, on) for (x, y, on) in pts]
    n = len(P)
    if n == 0:
        return []
    if P[0][2]:
        rot = P
        start = (P[0][0], P[0][1])
        j = 1
    elif P[-1][2]:
        rot = P[-1:] + P[:-1]
        start = (P[-1][0], P[-1][1])
        j = 1
    else:
        rot = P
        start = ((P[-1][0] + P[0][0]) / 2, (P[-1][1] + P[0][1]) / 2)
        j = 0
    out = [start]
    cur = start
    m = len(rot)
    while j < m:
        x, y, on = rot[j]
        if on:
            out.append((x, y))
            cur = (x, y)
            j += 1
        else:
            k = (j + 1) % m
            nx, ny, non = rot[k]
            if non:
                _quad(out, cur, (x, y), (nx, ny))
                cur = (nx, ny)
                j += 2
            else:
                mx, my = (x + nx) / 2, (y + ny) / 2
                _quad(out, cur, (x, y), (mx, my))
                cur = (mx, my)
                j += 1
    return out


def _render_glyph_mask(fid, cp, size):
    """Return (advance_px, w, h, xoff, yoff, alpha) for one glyph.

    All contours of the glyph are filled in ONE even-odd scanline pass,
    so O/o/0/a/e/D/8 render hollow. xoff/yoff are the bitmap origin
    relative to the pen position on the baseline (y down).
    """
    if (fid, cp) not in GLYPHS:
        cp = 63
        if (fid, cp) not in GLYPHS:
            return (0.0, 0, 0, 0, 0, bytearray())
    adv, contours = GLYPHS[(fid, cp)]
    scale = size * SS / UPM
    polys = [_flatten(c, scale) for c in contours]
    xs = [p[0] for poly in polys for p in poly]
    ys = [p[1] for poly in polys for p in poly]
    if not xs:
        return (adv * size / UPM, 0, 0, 0, 0, bytearray())
    # Snap bbox to SS multiples so the downsampled origin is integral.
    x0 = int(math.floor(min(xs) / SS)) * SS
    x1 = int(math.ceil(max(xs) / SS)) * SS
    y0 = int(math.floor(min(ys) / SS)) * SS
    y1 = int(math.ceil(max(ys) / SS)) * SS
    w, h = x1 - x0, y1 - y0
    edges = []
    for poly in polys:
        for i in range(len(poly)):
            ax, ay = poly[i]
            bx, by = poly[(i + 1) % len(poly)]
            if ay == by:
                continue
            edges.append((ax, ay, bx, by))
    mask2 = bytearray(w * h)
    for row in range(h):
        yc = y0 + row + 0.5
        xi = []
        for (ax, ay, bx, by) in edges:
            if (ay <= yc < by) or (by <= yc < ay):
                t = (yc - ay) / (by - ay)
                xi.append(ax + t * (bx - ax))
        xi.sort()
        for k in range(0, len(xi) - 1, 2):
            px0 = max(0, int(math.ceil(xi[k] - x0 - 0.5)))
            px1 = min(w, int(math.ceil(xi[k + 1] - x0 - 0.5)))
            for px in range(px0, px1):
                mask2[row * w + px] = 1
    ow, oh = w // SS, h // SS
    alpha = bytearray(ow * oh)
    for j in range(oh):
        for i in range(ow):
            s = 0
            for dy in range(SS):
                base = (j * SS + dy) * w + i * SS
                for dx in range(SS):
                    s += mask2[base + dx]
            alpha[j * ow + i] = min(255, s * 255 // (SS * SS))
    return (adv * size / UPM, ow, oh, x0 // SS, y0 // SS, alpha)


_GLYPH_CACHE = {}


def _glyph(fid, cp, size):
    key = (fid, cp, size)
    m = _GLYPH_CACHE.get(key)
    if m is None:
        m = _render_glyph_mask(fid, cp, size)
        _GLYPH_CACHE[key] = m
    return m


def text_width(s, size, bold=False):
    fid = "B" if bold else "R"
    w = 0.0
    for ch in s:
        w += _glyph(fid, ord(ch), size)[0]
    return w


def wrap_text(s, size, bold, max_w):
    lines = []
    cur = ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, size, bold) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.buf), 3):
            self.buf[i] = r
            self.buf[i + 1] = g
            self.buf[i + 2] = b

    def set_px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, int(x))
        y0 = max(0, int(y))
        x1 = min(self.w, int(x + w))
        y1 = min(self.h, int(y + h))
        if x1 <= x0 or y1 <= y0:
            return
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.buf[i] = r
                self.buf[i + 1] = g
                self.buf[i + 2] = b

    def blit_alpha(self, bx, by, gw, gh, alpha, color):
        r, g, b = color
        for j in range(gh):
            yy = by + j
            if yy < 0 or yy >= self.h:
                continue
            for i in range(gw):
                a = alpha[j * gw + i]
                if a == 0:
                    continue
                xx = bx + i
                if xx < 0 or xx >= self.w:
                    continue
                k = (yy * self.w + xx) * 3
                if a == 255:
                    self.buf[k] = r
                    self.buf[k + 1] = g
                    self.buf[k + 2] = b
                else:
                    self.buf[k] = (r * a + self.buf[k] * (255 - a)) // 255
                    self.buf[k + 1] = (g * a + self.buf[k + 1] * (255 - a)) // 255
                    self.buf[k + 2] = (b * a + self.buf[k + 2] * (255 - a)) // 255

    def text(self, x, y, s, size, bold, color, align="left"):
        """Draw text; x, y is the baseline point (left/center/right)."""
        fid = "B" if bold else "R"
        w = text_width(s, size, bold)
        if align == "center":
            x -= w / 2
        elif align == "right":
            x -= w
        pen = x
        for ch in s:
            adv, gw, gh, xoff, yoff, alpha = _glyph(fid, ord(ch), size)
            if gw and gh:
                bx = int(round(pen + xoff))
                by = int(round(y + yoff))
                self.blit_alpha(bx, by, gw, gh, alpha, color)
            pen += adv
        return w

    def line(self, x0, y0, x1, y1, color, width=1):
        dx, dy = x1 - x0, y1 - y0
        length = math.hypot(dx, dy)
        if length == 0:
            return
        nx, ny = -dy / length * width / 2, dx / length * width / 2
        self.fill_poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny),
                        (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], color)

    def fill_poly(self, pts, color):
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        y0 = max(0, int(math.floor(min(ys))))
        y1 = min(self.h, int(math.ceil(max(ys))))
        edges = []
        for i in range(len(pts)):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % len(pts)]
            if ay == by:
                continue
            edges.append((ax, ay, bx, by))
        r, g, b = color
        for yy in range(y0, y1):
            yc = yy + 0.5
            xs = []
            for (ax, ay, bx, by) in edges:
                if (ay <= yc < by) or (by <= yc < ay):
                    t = (yc - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                xa = max(0, int(math.ceil(xs[k] - 0.5)))
                xb = min(self.w, int(math.ceil(xs[k + 1] - 0.5)))
                for xx in range(xa, xb):
                    i = (yy * self.w + xx) * 3
                    self.buf[i] = r
                    self.buf[i + 1] = g
                    self.buf[i + 2] = b

    def circle(self, cx, cy, r, color):
        for yy in range(int(cy - r), int(cy + r) + 1):
            dy = yy - cy
            dx = math.sqrt(max(0, r * r - dy * dy))
            self.fill_rect(cx - dx, yy, 2 * dx, 1, color)

    def ring(self, cx, cy, r_out, r_in, color):
        for yy in range(int(cy - r_out), int(cy + r_out) + 1):
            dy = yy - cy
            dxo = math.sqrt(max(0, r_out * r_out - dy * dy))
            dxi = math.sqrt(max(0, r_in * r_in - dy * dy)) if abs(dy) < r_in else 0
            if dxi > 0:
                self.fill_rect(cx - dxo, yy, dxo - dxi, 1, color)
                self.fill_rect(cx + dxi, yy, dxo - dxi, 1, color)
            else:
                self.fill_rect(cx - dxo, yy, 2 * dxo, 1, color)


def _png_chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def write_png(cv, path):
    w, h = cv.w, cv.h
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += cv.buf[y * w * 3:(y + 1) * w * 3]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", ihdr)
    png += _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _png_chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
PANEL = (238, 232, 216)
INK = (26, 26, 26)
INK_SOFT = (78, 76, 68)
DECK_GREY = (58, 56, 50)  # v1.3: small-card deck only, darker than INK_SOFT
TEAL = (15, 76, 76)
TEAL_DK = (10, 52, 52)
NAVY = (20, 33, 61)
NAVY_LT = (52, 70, 104)
RED = (178, 34, 34)
AMBER = (168, 116, 0)
BLUE = (36, 80, 140)
GREY = (96, 94, 86)
RULE = (198, 190, 170)
LAND = (214, 226, 220)
WHITE = (255, 255, 255)
CREAM = (240, 234, 214)

PILL_COLOR = {"CONFIRMED": TEAL, "CLAIM": RED, "REPORTED": AMBER,
              "ONGOING": BLUE, "SCHEDULED": GREY}

# ---------------------------------------------------------------- content
# (head, deck, pill, kicker)
LEADS = [
    ("ASIAN TECH ROUT: NIKKEI \u22123.6%, KOSPI \u22125.6%",
     "Taiex \u22126%+, SoftBank \u221216.1%, TSMC \u22128.1% as AI-spending doubts spread. "
     "US fell Tue; Dow still topped 50,000.",
     "CONFIRMED", "MARKETS \u00b7 ASIA-PACIFIC"),
    ("CHINA LAUNCHES SHENZHOU-24; FIRST PAKISTANI IN ORBIT",
     "Long March 2F lifts off 00:18 UTC, docks with Tiangong ~3.5h later. "
     "Muhammad Zeeshan Ali, 40, first foreigner on China's station; crew stays 5\u201310 days.",
     "CONFIRMED", "SPACE \u00b7 CHINA"),
    ("HORMUZ: TWO MORE TANKERS HIT MINES, IRAN SAYS",
     "IRGC Navy claims 2 more tankers hit mines early Wed; Tehran says it downed "
     "2 drones. No US confirmation yet; strait stays closed day by day.",
     "CLAIM", "CONFLICT \u00b7 STRAIT OF HORMUZ"),
]

# (head, deck, pill, icon)
SMALL = [
    ("AUSTRALIA CPI JUMPS TO +4.9%",
     "Oct CPI up from 4.3%; fuel +6.3%. RBA 4.85%; ASX +1.35%.",
     "CONFIRMED", "cpi"),
    ("BANGLADESH GARMENT PAY +36%",
     "17,000 taka ($139) at 2am Wed; 4m workers, 80% exports.",
     "CONFIRMED", "wage"),
    ("SOLOMONS SIGNS AUSTRALIA PACT",
     "Australia primary partner; no foreign base. A$740m aid.",
     "CONFIRMED", "treaty"),
    ("CARTAGENA STANDOFF DRAGS ON",
     "10 of ~30 freed; ~20 still held Wed; president at scene.",
     "ONGOING", "store"),
    ("TRUMP READIES TARIFFS ON 16",
     "USTR findings due Tue\u2013Wed; rates unclear.",
     "REPORTED", "ship"),
    ("N. KOREA EXPELS SWISS ENVOY",
     "48 hours to leave; Pyongyang office shut after 37 days.",
     "CONFIRMED", "flag"),
    ("SYDNEY DOUBLE MURDER GUILTY",
     "Ex-cop convicted over 2024 killings; sentencing Mar 2027.",
     "CONFIRMED", "gavel"),
    ("26 TRAPPED IN BOGOR GOLD MINE",
     "Shaft flooded Mon; 11 of ~30 escaped; rescue blocked.",
     "CONFIRMED", "helmet"),
    ("IOWA TO BLAST 9,500 LB AZIDE",
     "68 barrels at 9am CT; plume 100+ miles; 5-mile cone.",
     "SCHEDULED", "blast"),
    ("KOREA BIRTHS JUMP +12.2%",
     "Sept births 25,113; fertility 0.90; 27th straight rise.",
     "CONFIRMED", "birth"),
]

ALSO = [
    "TSMC \u22128.1% in Taiwan chip rout",
    "Samsung \u22129.1%; SK Hynix \u22128.6%",
    "Kioxia \u221215.4% in Tokyo sell-off",
    "Iran says it downed 2 drones",
    "Hang Seng +1% as Asia sinks",
    "Brent \u221221% in Nov, at $87.49",
    "Sensex +1.8% as Asia sinks",
    "HK marks Tai Po fire, 168 dead",
    "Spix's macaw chick Hope hatches",
    "Brazil dengue \u221268% via mosquitoes",
    "Dragonfly Titan parts arrive",
    "Astronaut's wife gives birth",
    "Deepest eruptions in Mariana Trench",
    "New amphibian named Maria",
    "Blight-proof chestnut returns",
    "Microplastics in 95/120 Oman fish",
    "Oh Seung-ho in Naoki shortlist",
    "First Children's Booker shortlist",
    "Iwo Jima eruption adds new land",
    "18% of midlife women quit smoking",
    "Canada women win Para hockey 10-0",
    "MIT: tiny black holes may eat stars",
]

STATS = [
    ("\u22123.6%", "NIKKEI"),
    ("\u221216.1%", "SOFTBANK"),
    ("+4.9%", "AU CPI"),
    ("+36%", "GARMENT PAY"),
    ("+12.2%", "KOREA BIRTHS"),
    ("26", "TRAPPED MINERS"),
]

TIMELINE = [
    ("00:18 UTC", "Shenzhou-24 lifts off"),
    ("00:30 UTC", "Australia CPI: +4.9%"),
    ("03:10 UTC", "Korea births data out"),
    ("05:17 UTC", "10 hostages freed, Cartagena"),
    ("05:23 UTC", "Iran: 2 more tankers hit"),
    ("15:00 UTC", "Iowa azide blast, 9am CT"),
]

# (name, lat, lon, label?)
PINS = [
    ("Tokyo", 35.7, 139.7, True),
    ("Seoul", 37.6, 127.0, True),
    ("Taipei", 25.0, 121.6, False),
    ("Jiuquan", 40.0, 100.0, False),
    ("Hormuz", 26.5, 56.5, True),
    ("Canberra", -35.3, 149.1, True),
    ("Dhaka", 23.8, 90.4, False),
    ("Cartagena", 10.4, -75.5, True),
    ("Pyongyang", 39.0, 125.8, False),
    ("Sydney", -33.9, 151.2, False),
    ("Bogor", -6.6, 106.8, False),
    ("Iowa", 40.8, -91.3, True),
    ("Washington", 38.9, -77.0, False),
]

DATECHECK = [
    "Houthi hits Riyadh PIF Tower, 11 hurt \u2014 Tue 24 Nov",
    "Nvidia \u22127%; Huang in therapy \u2014 Tue 24 Nov",
    "Huawei guilty on 10 of 12 counts \u2014 Tue 24 Nov",
    "Hamas security chief killed in Gaza \u2014 Tue 24 Nov",
    "CIA/ODNI unclassified breach \u2014 Tue 24 Nov",
    "Democrats reach 259 House seats \u2014 Tue 24 Nov",
    "Cuba life expectancy 78.8 to 74.4 \u2014 Tue 24 Nov",
    "Ronaldo's 987th goal \u2014 Tue 24 Nov",
    "Sooryavanshi 204 off 53 balls \u2014 Tue 24 Nov",
    "RAK bus crash kills 13 \u2014 Tue 24 Nov",
    "Turkish heli crash kills 5 \u2014 Tue 24 Nov",
    "BepiColombo enters Mercury orbit \u2014 Sat 21 Nov",
]

REGION_LINE = ("ASIA-PACIFIC 14 \u00b7 MIDDLE EAST 4 \u00b7 AMERICAS 10 \u00b7 "
               "OCEANIA 4 \u00b7 EUROPE 2 \u00b7 WORLD 1 \u2014 13 PLACES PINNED")

# Simplified continent outlines (lon, lat), equirectangular schematic.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-145, 60), (-165, 60)],
    [(-80, 10), (-70, 12), (-60, 5), (-50, 0), (-40, -5), (-35, -10),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -55),
     (-73, -40), (-75, -20), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
     (30, -30), (20, -35), (15, -30), (12, -18), (13, -5), (9, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (0, 44), (10, 44), (20, 40), (26, 38),
     (30, 36), (36, 36), (40, 38), (45, 40), (50, 45), (55, 50),
     (60, 55), (65, 60), (70, 70), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 60),
     (142, 55), (140, 45), (135, 43), (130, 38), (127, 35), (122, 32),
     (120, 28), (115, 23), (110, 20), (108, 15), (105, 10), (100, 8),
     (98, 12), (95, 16), (92, 21), (90, 22), (85, 20), (80, 15),
     (77, 8), (75, 12), (72, 20), (68, 23), (65, 25), (60, 25),
     (57, 26), (54, 27), (50, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (33, 36), (30, 36), (26, 38), (22, 37), (18, 40),
     (15, 38), (12, 42), (8, 44), (3, 43), (-2, 37), (-6, 36), (-9, 38)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
     (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20), (114, -22)],
]


# ---------------------------------------------------------------- helpers
def pill(cv, x, y, label, size=9):
    """Certainty pill: filled rect + white bold label. Returns width."""
    w = int(text_width(label, size, True)) + 12
    h = size + 7
    color = PILL_COLOR[label]
    cv.fill_rect(x, y, w, h, color)
    cv.text(x + 6, y + h - 4, label, size, True, WHITE)
    return w


def draw_pill_right(cv, x_right, y, label, size=9):
    w = int(text_width(label, size, True)) + 12
    pill(cv, x_right - w, y, label, size)
    return w


# ---------------------------------------------------------------- icons
def icon_chart(cv, x, y, s):
    # falling line + descending bars, red down arrow
    cv.line(x + 4, y + s - 8, x + s - 4, y + s - 8, INK_SOFT, 1)
    cv.line(x + 4, y + 6, x + 4, y + s - 8, INK_SOFT, 1)
    bw = (s - 14) // 5
    heights = [s - 26, s - 32, s - 40, s - 48, s - 56]
    for i, hh in enumerate(heights):
        bx = x + 8 + i * (bw + 2)
        cv.fill_rect(bx, y + s - 8 - hh, bw, hh, TEAL if i < 2 else RED)
    pts = [(x + 8, y + 16), (x + s // 3, y + 26), (x + 2 * s // 3, y + 38),
           (x + s - 8, y + s - 16)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 3)
    cv.fill_poly([(x + s - 14, y + s - 22), (x + s - 4, y + s - 22),
                  (x + s - 9, y + s - 12)], RED)


def icon_rocket(cv, x, y, s):
    # orbit ring + station + rocket
    cx, cy = x + s // 2, y + s // 2
    cv.ring(cx, cy, s // 2 - 2, s // 2 - 6, TEAL)
    cv.fill_rect(cx - 12, cy - 4, 24, 8, INK)
    cv.fill_rect(cx - 20, cy - 2, 8, 4, TEAL)
    cv.fill_rect(cx + 12, cy - 2, 8, 4, TEAL)
    rx, ry = x + s - 22, y + 8
    cv.fill_poly([(rx, ry), (rx + 8, ry + 12), (rx + 4, ry + 12),
                  (rx + 4, ry + 26), (rx, ry + 26), (rx, ry + 12)], INK)
    cv.fill_poly([(rx - 4, ry + 20), (rx, ry + 14), (rx, ry + 26)], RED)
    cv.fill_poly([(rx + 8, ry + 20), (rx + 8, ry + 14), (rx + 4, ry + 26)], RED)
    cv.fill_poly([(rx + 1, ry + 26), (rx + 7, ry + 26), (rx + 4, ry + 34)], AMBER)
    for (sx, sy) in ((x + 6, y + 12), (x + 12, y + s - 10), (x + s - 6, y + s - 14)):
        cv.circle(sx, sy, 1, TEAL)


def icon_strait(cv, x, y, s):
    # two land masses, narrow strait, two tankers, mine dots
    cv.fill_poly([(x, y), (x + s, y), (x + s, y + s // 3 - 4),
                  (x + s * 2 // 3, y + s // 3 + 2), (x + s // 3, y + s // 3 - 4),
                  (x, y + s // 3 + 2)], LAND)
    cv.fill_poly([(x, y + 2 * s // 3), (x + s // 3, y + 2 * s // 3 - 2),
                  (x + 2 * s // 3, y + 2 * s // 3 + 4), (x + s, y + 2 * s // 3 - 2),
                  (x + s, y + s), (x, y + s)], LAND)
    cv.fill_rect(x, y + s // 3 + 2, s, s // 3, (120, 170, 175))
    # tankers
    cv.fill_rect(x + 8, y + s // 2 - 3, 22, 7, INK)
    cv.fill_rect(x + 24, y + s // 2 - 8, 6, 5, INK)
    cv.fill_rect(x + s - 34, y + s // 2 + 2, 22, 7, INK)
    cv.fill_rect(x + s - 18, y + s // 2 - 3, 6, 5, INK)
    # mines
    for (mx, my) in ((x + s // 2 - 2, y + s // 2 - 10),
                     (x + s // 2 + 8, y + s // 2 + 10)):
        cv.circle(mx, my, 3, RED)
        cv.line(mx - 5, my, mx + 5, my, RED, 1)
        cv.line(mx, my - 5, mx, my + 5, RED, 1)


def icon_cpi(cv, x, y, s):
    cv.text(x + s // 2 - 2, y + s - 8, "%", 26, True, TEAL, align="center")
    cv.line(x + s - 12, y + 10, x + s - 4, y + 2, RED, 2)
    cv.fill_poly([(x + s - 14, y + 4), (x + s - 4, y + 4), (x + s - 9, y + 12)], RED)


def icon_wage(cv, x, y, s):
    cv.fill_rect(x + 2, y + s // 2 - 9, s - 4, 18, PANEL)
    cv.line(x + 2, y + s // 2 - 9, x + s - 2, y + s // 2 - 9, TEAL, 2)
    cv.line(x + 2, y + s // 2 + 9, x + s - 2, y + s // 2 + 9, TEAL, 2)
    cv.line(x + 2, y + s // 2 - 9, x + 2, y + s // 2 + 9, TEAL, 2)
    cv.line(x + s - 2, y + s // 2 - 9, x + s - 2, y + s // 2 + 9, TEAL, 2)
    cv.text(x + s // 2, y + s // 2 + 7, "$", 18, True, TEAL, align="center")
    cv.circle(x + s - 6, y + 6, 3, RED)


def icon_treaty(cv, x, y, s):
    cv.fill_rect(x + 6, y + 2, s - 14, s - 6, WHITE)
    cv.line(x + 6, y + 2, x + s - 8, y + 2, INK, 1)
    cv.line(x + 6, y + s - 4, x + s - 8, y + s - 4, INK, 1)
    cv.line(x + 6, y + 2, x + 6, y + s - 4, INK, 1)
    cv.line(x + s - 8, y + 2, x + s - 8, y + s - 4, INK, 1)
    for i, yy in enumerate((y + 10, y + 16, y + 22)):
        cv.line(x + 10, yy, x + s - 14, yy, INK_SOFT, 1)
    cv.circle(x + s - 14, y + s - 12, 6, RED)
    cv.circle(x + s - 14, y + s - 12, 3, WHITE)


def icon_store(cv, x, y, s):
    cv.fill_rect(x + 4, y + 12, s - 8, s - 16, PANEL)
    cv.line(x + 4, y + 12, x + s - 4, y + 12, INK, 2)
    for i in range(4):
        bx = x + 6 + i * ((s - 12) // 4)
        cv.fill_poly([(bx, y + 2), (bx + (s - 12) // 8, y + 2),
                      (bx + (s - 12) // 8, y + 12), (bx, y + 12)],
                     RED if i % 2 == 0 else WHITE)
    for i in range(3):
        bx = x + 10 + i * 8
        cv.line(bx, y + 16, bx, y + s - 6, RED, 2)
    cv.fill_rect(x + s // 2 - 3, y + s - 8, 6, 4, INK)


def icon_ship(cv, x, y, s):
    cv.fill_poly([(x + 2, y + s - 12), (x + s - 2, y + s - 12),
                  (x + s - 8, y + s - 2), (x + 8, y + s - 2)], INK)
    cv.fill_rect(x + 6, y + s - 24, 10, 10, TEAL)
    cv.fill_rect(x + 18, y + s - 24, 10, 10, RED)
    cv.fill_rect(x + 11, y + s - 34, 12, 10, AMBER)
    cv.text(x + s - 8, y + 12, "%", 14, True, TEAL)


def icon_flag(cv, x, y, s):
    cv.line(x + 6, y + 2, x + 6, y + s - 2, INK, 2)
    cv.fill_poly([(x + 6, y + 2), (x + s - 6, y + 8), (x + 6, y + 14)], RED)
    cv.line(x + s - 12, y + s - 12, x + s - 2, y + s - 2, RED, 2)
    cv.line(x + s - 2, y + s - 12, x + s - 12, y + s - 2, RED, 2)


def icon_gavel(cv, x, y, s):
    cv.line(x + 6, y + s - 8, x + s - 6, y + s - 8, INK, 2)
    cv.line(x + 10, y + s - 12, x + s - 12, y + 8, INK, 3)
    cv.fill_rect(x + s - 16, y + 2, 12, 8, TEAL)
    cv.fill_rect(x + 4, y + s - 20, 10, 7, TEAL)


def icon_helmet(cv, x, y, s):
    cx, cy = x + s // 2, y + s // 2 + 2
    cv.fill_poly([(cx - 12, cy + 2), (cx - 12, cy - 4), (cx - 8, cy - 10),
                  (cx + 8, cy - 10), (cx + 12, cy - 4), (cx + 12, cy + 2)],
                 AMBER)
    cv.fill_rect(cx - 14, cy + 2, 28, 3, AMBER)
    cv.circle(cx, cy - 6, 2, WHITE)
    cv.line(cx - 4, cy + 8, cx + 4, cy + 8, INK_SOFT, 1)
    cv.line(cx - 4, cy + 8, cx - 4, cy + 12, INK_SOFT, 1)
    cv.line(cx + 4, cy + 8, cx + 4, cy + 12, INK_SOFT, 1)


def icon_blast(cv, x, y, s):
    cx, cy = x + s // 2, y + s // 2 - 4
    pts = []
    for i in range(12):
        ang = math.pi * i / 6
        r = s // 2 - 4 if i % 2 == 0 else s // 4
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    cv.fill_poly(pts, AMBER)
    cv.circle(cx, cy, 5, RED)
    cv.fill_rect(x + s // 2 - 8, y + s - 12, 16, 10, INK)
    cv.line(x + s // 2 - 8, y + s - 9, x + s // 2 + 8, y + s - 9, WHITE, 1)
    cv.line(x + s // 2 - 8, y + s - 5, x + s // 2 + 8, y + s - 5, WHITE, 1)


def icon_birth(cv, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    cv.circle(cx - 4, cy - 8, 6, TEAL)
    cv.fill_poly([(cx - 14, cy - 2), (cx + 6, cy - 2), (cx + 2, cy + 10),
                  (cx - 10, cy + 10)], (120, 170, 175))
    cv.line(cx - 14, cy - 2, cx - 18, cy - 8, TEAL, 2)
    cv.line(cx + 6, cy - 2, cx + 10, cy - 8, TEAL, 2)
    cv.text(x + s - 8, y + s - 4, "+", 16, True, RED)


ICONS = {"chart": icon_chart, "rocket": icon_rocket, "strait": icon_strait,
         "cpi": icon_cpi, "wage": icon_wage, "treaty": icon_treaty,
         "store": icon_store, "ship": icon_ship, "flag": icon_flag,
         "gavel": icon_gavel, "helmet": icon_helmet, "blast": icon_blast,
         "birth": icon_birth}
LEAD_ICONS = ["chart", "rocket", "strait"]

# ---------------------------------------------------------------- layout
W, H = 1024, 1024
M = 28            # side margin
R = 996           # right edge (1024 - 28)
CW = 968          # content width


def rect_outline(cv, x, y, w, h, color, width=1):
    cv.fill_rect(x, y, w, width, color)
    cv.fill_rect(x, y + h - width, w, width, color)
    cv.fill_rect(x, y, width, h, color)
    cv.fill_rect(x + w - width, y, width, h, color)


def draw_masthead(cv):
    cv.text(512, 50, "THE WEDNESDAY GLOBE", 34, True, INK, align="center")
    cv.text(512, 68, "WEDNESDAY 25 NOVEMBER 2026 \u00b7 35 STORIES "
            "\u00b7 FIRST REPORTED OR DEVELOPING TODAY", 11, True, TEAL,
            align="center")
    cv.fill_rect(M, 74, CW, 2, INK)
    cv.fill_rect(M, 78, CW, 1, INK)


def draw_stats(cv):
    cv.fill_rect(M, 84, CW, 56, NAVY)
    for i, (num, label) in enumerate(STATS):
        cx = M + (i + 0.5) * CW / 6
        cv.text(cx, 118, num, 26, True, WHITE, align="center")
        cv.text(cx, 136, label, 10, False, CREAM, align="center")
        if i:
            x = int(M + i * CW / 6)
            cv.fill_rect(x, 92, 1, 40, NAVY_LT)


def draw_region(cv):
    cv.text(512, 158, REGION_LINE, 11, True, INK, align="center")


def draw_leads(cv):
    for i, (head, deck, p, kicker) in enumerate(LEADS):
        y0 = 168 + i * 100
        # art box
        cv.fill_rect(M, y0 + 2, 96, 96, PANEL)
        rect_outline(cv, M, y0 + 2, 96, 96, RULE, 1)
        ICONS[LEAD_ICONS[i]](cv, M + 6, y0 + 8, 84)
        # kicker + pill
        cv.text(140, y0 + 16, kicker, 10, True, TEAL)
        draw_pill_right(cv, R, y0 + 2, p)
        # head + deck
        cv.text(140, y0 + 40, head, 20, True, INK)
        lines = wrap_text(deck, 13, False, R - 140)
        for k, ln in enumerate(lines[:2]):
            cv.text(140, y0 + 62 + k * 16, ln, 13, False, INK)
        if i < 2:
            cv.fill_rect(M, y0 + 100, CW, 1, RULE)


def draw_timeline(cv):
    cv.text(M, 486, "THE DAY IN SIX MOMENTS", 11, True, TEAL)
    cv.fill_rect(50, 511, 895, 2, TEAL)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 70 + i * 171
        cv.circle(cx, 512, 4, TEAL)
        cv.text(cx, 502, t, 11, True, INK, align="center")
        lines = wrap_text(label, 10, False, 170)
        for k, ln in enumerate(lines[:2]):
            cv.text(cx, 526 + k * 11, ln, 10, True, INK, align="center")


def draw_small(cv):
    for r in range(2):
        for c in range(5):
            idx = r * 5 + c
            head, deck, p, icon = SMALL[idx]
            x = M + c * 195
            y0 = 544 + r * 108
            rect_outline(cv, x, y0, 187, 108, RULE, 1)
            # v1.3 polish: treaty +3px, ship +2px (both land at 9px clearance)
            # v1.6 polish: even ink-top clearance to ~10px — the five 8px
            # icons (+2: cpi/store/flag/gavel/blast); helmet -4px (was 16px,
            # optical centre 26.5 -> 23, dead-centre of the pack). Bottom
            # gaps after: flag 4px (tightest), ship 5px, rest 7-13px.
            dy = {"treaty": 3, "ship": 2, "cpi": 2, "store": 2, "flag": 2,
                  "gavel": 2, "blast": 2, "helmet": -4}.get(icon, 0)
            ICONS[icon](cv, x + 75, y0 + 6 + dy, 36)
            draw_pill_right(cv, x + 182, y0 + 5, p)
            hl = wrap_text(head, 15, True, 171)
            for k, ln in enumerate(hl[:2]):
                cv.text(x + 93, y0 + 56 + k * 18, ln, 15, True, INK,
                        align="center")
            dl = wrap_text(deck, 10, False, 171)
            for k, ln in enumerate(dl[:2]):
                cv.text(x + 93, y0 + 88 + k * 13, ln, 10, False, DECK_GREY,
                        align="center")


def draw_also(cv):
    cv.text(M, 782, "ALSO IN THE DAY", 12, True, TEAL)
    for i, item in enumerate(ALSO):
        col, row = divmod(i, 11)
        x = M + col * 268
        y = 800 + row * 13
        cv.fill_rect(x, y - 8, 3, 3, TEAL)
        cv.text(x + 8, y, item, 11, True, INK)


def _project(lon, lat):
    x = 568 + (lon + 170) / 360 * 428
    y = 790 + (85 - lat) / 145 * 142
    return x, y


LABEL_DX = {"Tokyo": (6, -6, "left"), "Seoul": (-10, 9, "right"),
            "Hormuz": (4, -11, "left"), "Canberra": (-6, 12, "right"),
            "Iowa": (6, -6, "left"), "Cartagena": (-6, 12, "right")}


def draw_map(cv):
    cv.text(568, 782, "WHERE IT HAPPENED \u2014 13 PLACES", 12, True, TEAL)
    rect_outline(cv, 568, 790, 428, 142, RULE, 1)
    for cont in CONTINENTS:
        pts = [_project(lon, lat) for (lon, lat) in cont]
        cv.fill_poly(pts, LAND)
        for i in range(len(pts)):
            ax, ay = pts[i]
            bx, by = pts[(i + 1) % len(pts)]
            cv.line(ax, ay, bx, by, TEAL, 1)
    for (name, lat, lon, labelled) in PINS:
        x, y = _project(lon, lat)
        cv.circle(x, y, 3, RED)
        cv.circle(x, y, 1, WHITE)
        if labelled:
            dx, dy, al = LABEL_DX[name]
            cv.text(x + dx, y + dy, name.upper(), 9, True, TEAL,
                    align=al)


def draw_datecheck(cv):
    rect_outline(cv, M, 936, CW, 70, RED, 2)
    cv.text(36, 950, "DATE CHECK \u2014 PICTURED ELSEWHERE AS TODAY'S NEWS. "
            "THESE ARE NOT.", 12, True, RED)
    cv.text(988, 950, "+35 MORE CHECKED", 10, True, RED, align="right")
    for i, item in enumerate(DATECHECK):
        col, row = divmod(i, 4)
        x = 36 + col * 316
        y = 962 + row * 11
        cv.text(x, y, item, 10, True, INK)


def draw_footer(cv):
    cv.text(512, 1016,
            "Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 Al Jazeera \u00b7 Yonhap "
            "\u00b7 ABS \u00b7 Mehr \u00b7 One Turn \u2014 All stories first reported or developing "
            "Wed 25 Nov 2026 unless dated in DATE CHECK \u00b7 Rendered by code, "
            "no photos",
            9, False, INK, align="center")


def build():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_stats(cv)
    draw_region(cv)
    draw_leads(cv)
    draw_timeline(cv)
    draw_small(cv)
    draw_also(cv)
    draw_map(cv)
    draw_datecheck(cv)
    draw_footer(cv)
    return cv


def main():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out, exist_ok=True)
    cv = build()
    path = os.path.join(out, "entry.png")
    n = write_png(cv, path)
    print("wrote %s %d bytes" % (path, n))


if __name__ == "__main__":
    main()
