/**
 * Financial Dashboard - Main JavaScript
 * Market Data & Chart Logic
 */

const marketData = {
  indices: [
    {
      code: '000001.SH',
      name: '上证指数',
      currency: 'CNY',
      data: [
        { date: '2024-01-02', open: 2962.28, high: 2976.54, low: 2958.33, close: 2967.25, volume: 32456789 },
        { date: '2024-01-03', open: 2965.12, high: 2982.45, low: 2959.88, close: 2978.67, volume: 35678901 },
        { date: '2024-01-04', open: 2975.33, high: 2995.12, low: 2970.55, close: 2988.45, volume: 38901234 },
        { date: '2024-01-05', open: 2985.67, high: 2998.34, low: 2978.22, close: 2982.12, volume: 41234567 },
        { date: '2024-01-08', open: 2980.45, high: 3012.78, low: 2975.33, close: 3008.56, volume: 45678901 },
        { date: '2024-01-09', open: 3005.22, high: 3018.44, low: 2998.67, close: 3015.33, volume: 42345678 },
        { date: '2024-01-10', open: 3012.88, high: 3025.66, low: 3005.12, close: 3022.45, volume: 47890123 },
        { date: '2024-01-11', open: 3018.55, high: 3038.22, low: 3012.44, close: 3035.67, volume: 51234567 },
        { date: '2024-01-12', open: 3032.11, high: 3045.88, low: 3025.33, close: 3041.22, volume: 48901234 },
        { date: '2024-01-15', open: 3038.77, high: 3052.44, low: 3030.55, close: 3048.88, volume: 52345678 },
        { date: '2024-01-16', open: 3045.22, high: 3058.66, low: 3038.11, close: 3055.44, volume: 55678901 },
        { date: '2024-01-17', open: 3052.88, high: 3065.33, low: 3045.22, close: 3062.11, volume: 58901234 },
        { date: '2024-01-18', open: 3058.55, high: 3072.44, low: 3050.66, close: 3068.77, volume: 61234567 },
        { date: '2024-01-19', open: 3065.22, high: 3078.88, low: 3058.33, close: 3075.44, volume: 59876543 },
        { date: '2024-01-22', open: 3072.11, high: 3085.66, low: 3065.22, close: 3082.33, volume: 62345678 },
        { date: '2024-01-23', open: 3078.55, high: 3092.44, low: 3070.11, close: 3088.77, volume: 65678901 },
        { date: '2024-01-24', open: 3085.22, high: 3098.88, low: 3078.55, close: 3095.44, volume: 68901234 },
        { date: '2024-01-25', open: 3092.11, high: 3105.66, low: 3085.22, close: 3102.33, volume: 71234567 },
        { date: '2024-01-26', open: 3098.55, high: 3112.44, low: 3090.11, close: 3108.77, volume: 69876543 },
        { date: '2024-01-29', open: 3105.22, high: 3118.88, low: 3098.55, close: 3115.44, volume: 72345678 },
        { date: '2024-01-30', open: 3112.11, high: 3125.66, low: 3105.22, close: 3122.33, volume: 75678901 },
        { date: '2024-01-31', open: 3118.55, high: 3132.44, low: 3110.11, close: 3128.77, volume: 78901234 },
        { date: '2024-02-01', open: 3125.22, high: 3138.88, low: 3118.55, close: 3135.44, volume: 81234567 },
        { date: '2024-02-02', open: 3132.11, high: 3145.66, low: 3125.22, close: 3142.33, volume: 79876543 },
        { date: '2024-02-05', open: 3128.44, high: 3138.22, low: 3115.66, close: 3122.55, volume: 85678901 },
        { date: '2024-02-06', open: 3118.33, high: 3132.44, low: 3108.22, close: 3128.66, volume: 82345678 },
        { date: '2024-02-07', open: 3125.55, high: 3142.33, low: 3118.44, close: 3138.77, volume: 88901234 },
        { date: '2024-02-08', open: 3135.22, high: 3152.88, low: 3128.55, close: 3148.44, volume: 91234567 },
        { date: '2024-02-19', open: 3142.66, high: 3165.22, low: 3135.44, close: 3158.33, volume: 95678901 },
        { date: '2024-02-20', open: 3155.44, high: 3172.88, low: 3148.22, close: 3168.55, volume: 98901234 }
      ],
      latest: { price: 3168.55, change: 10.22, changePercent: 0.32 },
      ma5: 3145.22,
      ma20: 3085.66,
      rsi: 62.5,
      macd: { dif: 25.33, dea: 18.77, macd: 13.12 }
    },
    {
      code: '399001.SZ',
      name: '深证成指',
      currency: 'CNY',
      data: [
        { date: '2024-01-02', open: 9425.33, high: 9458.22, low: 9418.55, close: 9448.66, volume: 28901234 },
        { date: '2024-01-03', open: 9442.11, high: 9475.44, low: 9435.22, close: 9468.33, volume: 31234567 },
        { date: '2024-01-04', open: 9462.55, high: 9495.88, low: 9455.11, close: 9488.77, volume: 33456789 },
        { date: '2024-01-05', open: 9482.22, high: 9508.44, low: 9468.66, close: 9478.55, volume: 35678901 },
        { date: '2024-01-08', open: 9472.33, high: 9518.22, low: 9465.44, close: 9508.66, volume: 38901234 },
        { date: '2024-01-09', open: 9502.11, high: 9535.44, low: 9495.22, close: 9525.33, volume: 41234567 },
        { date: '2024-01-10', open: 9518.55, high: 9548.88, low: 9512.33, close: 9542.77, volume: 43456789 },
        { date: '2024-01-11', open: 9535.22, high: 9568.44, low: 9528.66, close: 9558.11, volume: 45678901 },
        { date: '2024-01-12', open: 9552.33, high: 9578.55, low: 9545.22, close: 9568.44, volume: 47890123 },
        { date: '2024-01-15', open: 9562.11, high: 9592.44, low: 9555.33, close: 9585.66, volume: 50123456 },
        { date: '2024-01-16', open: 9578.55, high: 9608.88, low: 9572.22, close: 9602.33, volume: 52345678 },
        { date: '2024-01-17', open: 9595.22, high: 9622.44, low: 9588.66, close: 9618.77, volume: 54567890 },
        { date: '2024-01-18', open: 9612.33, high: 9638.55, low: 9605.11, close: 9628.44, volume: 56789012 },
        { date: '2024-01-19', open: 9622.11, high: 9648.44, low: 9615.22, close: 9638.77, volume: 54321098 },
        { date: '2024-01-22', open: 9632.55, high: 9658.88, low: 9625.33, close: 9652.11, volume: 56543210 },
        { date: '2024-01-23', open: 9645.22, high: 9672.44, low: 9638.66, close: 9665.33, volume: 58765432 },
        { date: '2024-01-24', open: 9658.33, high: 9685.55, low: 9652.11, close: 9678.44, volume: 60987654 },
        { date: '2024-01-25', open: 9672.11, high: 9698.44, low: 9665.22, close: 9688.77, volume: 63209876 },
        { date: '2024-01-26', open: 9682.55, high: 9708.88, low: 9675.33, close: 9698.11, volume: 65432098 },
        { date: '2024-01-29', open: 9692.22, high: 9718.44, low: 9685.66, close: 9708.33, volume: 67654321 },
        { date: '2024-01-30', open: 9702.11, high: 9728.55, low: 9695.22, close: 9718.44, volume: 69876543 },
        { date: '2024-01-31', open: 9712.33, high: 9738.88, low: 9705.11, close: 9728.66, volume: 72098765 },
        { date: '2024-02-01', open: 9722.55, high: 9748.22, low: 9715.44, close: 9738.33, volume: 74320987 },
        { date: '2024-02-02', open: 9732.11, high: 9758.44, low: 9725.66, close: 9748.77, volume: 76543210 },
        { date: '2024-02-05', open: 9718.33, high: 9742.55, low: 9702.11, close: 9715.22, volume: 78765432 },
        { date: '2024-02-06', open: 9708.22, high: 9735.44, low: 9695.33, close: 9722.11, volume: 80987654 },
        { date: '2024-02-07', open: 9718.55, high: 9745.88, low: 9708.22, close: 9735.66, volume: 83209876 },
        { date: '2024-02-08', open: 9728.22, high: 9758.44, low: 9718.55, close: 9748.33, volume: 85432098 },
        { date: '2024-02-19', open: 9738.11, high: 9772.22, low: 9728.44, close: 9762.55, volume: 87654321 },
        { date: '2024-02-20', open: 9752.44, high: 9785.88, low: 9742.22, close: 9775.33, volume: 89876543 }
      ],
      latest: { price: 9775.33, change: 12.78, changePercent: 0.13 },
      ma5: 9748.22,
      ma20: 9685.44,
      rsi: 58.3,
      macd: { dif: 18.55, dea: 12.33, macd: 12.44 }
    },
    {
      code: 'HSI',
      name: '恒生指数',
      currency: 'HKD',
      data: [
        { date: '2024-01-02', open: 17042.66, high: 17128.33, low: 17015.22, close: 17107.44, volume: 1234567890 },
        { date: '2024-01-03', open: 17095.11, high: 17185.44, low: 17068.22, close: 17156.88, volume: 1345678901 },
        { date: '2024-01-04', open: 17142.55, high: 17235.88, low: 17115.11, close: 17205.33, volume: 1456789012 },
        { date: '2024-01-05', open: 17192.22, high: 17268.44, low: 17165.66, close: 17185.55, volume: 1567890123 },
        { date: '2024-01-08', open: 17172.33, high: 17258.22, low: 17145.44, close: 17228.66, volume: 1678901234 },
        { date: '2024-01-09', open: 17215.11, high: 17305.44, low: 17188.22, close: 17278.33, volume: 1789012345 },
        { date: '2024-01-10', open: 17262.55, high: 17348.88, low: 17235.33, close: 17325.77, volume: 1890123456 },
        { date: '2024-01-11', open: 17312.22, high: 17398.44, low: 17285.66, close: 17378.11, volume: 2001234567 },
        { date: '2024-01-12', open: 17362.33, high: 17428.55, low: 17335.22, close: 17408.44, volume: 2112345678 },
        { date: '2024-01-15', open: 17395.11, high: 17475.44, low: 17368.33, close: 17448.66, volume: 2223456789 },
        { date: '2024-01-16', open: 17435.55, high: 17518.88, low: 17408.22, close: 17498.33, volume: 2334567890 },
        { date: '2024-01-17', open: 17485.22, high: 17558.44, low: 17458.66, close: 17538.77, volume: 2445678901 },
        { date: '2024-01-18', open: 17525.33, high: 17598.55, low: 17498.11, close: 17568.44, volume: 2556789012 },
        { date: '2024-01-19', open: 17555.11, high: 17628.44, low: 17528.22, close: 17598.77, volume: 2467890123 },
        { date: '2024-01-22', open: 17585.55, high: 17658.88, low: 17558.33, close: 17628.11, volume: 2578901234 },
        { date: '2024-01-23', open: 17615.22, high: 17688.44, low: 17588.66, close: 17658.33, volume: 2689012345 },
        { date: '2024-01-24', open: 17645.33, high: 17718.55, low: 17618.11, close: 17688.44, volume: 2800123456 },
        { date: '2024-01-25', open: 17675.11, high: 17748.44, low: 17648.22, close: 17718.77, volume: 2911234567 },
        { date: '2024-01-26', open: 17705.55, high: 17778.88, low: 17678.33, close: 17748.11, volume: 2822345678 },
        { date: '2024-01-29', open: 17735.22, high: 17808.44, low: 17708.66, close: 17778.33, volume: 2933456789 },
        { date: '2024-01-30', open: 17765.11, high: 17838.55, low: 17738.22, close: 17808.44, volume: 3044567890 },
        { date: '2024-01-31', open: 17795.33, high: 17868.88, low: 17768.11, close: 17838.66, volume: 3155678901 },
        { date: '2024-02-01', open: 17825.55, high: 17898.22, low: 17798.44, close: 17868.33, volume: 3266789012 },
        { date: '2024-02-02', open: 17855.11, high: 17928.44, low: 17828.66, close: 17898.77, volume: 3177890123 },
        { date: '2024-02-05', open: 17825.33, high: 17885.55, low: 17795.22, close: 17845.11, volume: 3288901234 },
        { date: '2024-02-06', open: 17835.22, high: 17898.44, low: 17805.33, close: 17865.66, volume: 3399012345 },
        { date: '2024-02-07', open: 17855.55, high: 17918.88, low: 17825.22, close: 17895.33, volume: 3510123456 },
        { date: '2024-02-08', open: 17885.22, high: 17948.44, low: 17855.55, close: 17925.77, volume: 3621234567 },
        { date: '2024-02-19', open: 17915.11, high: 17988.22, low: 17885.44, close: 17965.33, volume: 3732345678 },
        { date: '2024-02-20', open: 17955.44, high: 18018.88, low: 17925.22, close: 17998.55, volume: 3843456789 }
      ],
      latest: { price: 17998.55, change: 33.22, changePercent: 0.19 },
      ma5: 17955.33,
      ma20: 17865.44,
      rsi: 60.8,
      macd: { dif: 45.22, dea: 32.11, macd: 26.22 }
    },
    {
      code: 'DJI',
      name: '道琼斯',
      currency: 'USD',
      data: [
        { date: '2024-01-02', open: 37689.54, high: 37753.22, low: 37625.66, close: 37715.33, volume: 345678901 },
        { date: '2024-01-03', open: 37702.11, high: 37812.44, low: 37675.22, close: 37798.55, volume: 367890123 },
        { date: '2024-01-04', open: 37785.33, high: 37898.88, low: 37755.11, close: 37868.22, volume: 389012345 },
        { date: '2024-01-05', open: 37855.22, high: 37958.44, low: 37825.66, close: 37938.55, volume: 411234567 },
        { date: '2024-01-08', open: 37925.11, high: 38025.22, low: 37895.33, close: 37998.66, volume: 433456789 },
        { date: '2024-01-09', open: 37985.55, high: 38085.44, low: 37955.22, close: 38068.33, volume: 455678901 },
        { date: '2024-01-10', open: 38055.22, high: 38158.88, low: 38025.11, close: 38138.77, volume: 477890123 },
        { date: '2024-01-11', open: 38125.33, high: 38228.55, low: 38095.66, close: 38208.11, volume: 500012345 },
        { date: '2024-01-12', open: 38195.11, high: 38268.44, low: 38165.22, close: 38238.44, volume: 488234567 },
        { date: '2024-01-15', open: 38225.55, high: 38328.88, low: 38195.33, close: 38308.66, volume: 510456789 },
        { date: '2024-01-16', open: 38295.22, high: 38398.44, low: 38265.66, close: 38378.33, volume: 532678901 },
        { date: '2024-01-17', open: 38365.33, high: 38468.55, low: 38335.11, close: 38448.77, volume: 554890123 },
        { date: '2024-01-18', open: 38435.11, high: 38538.44, low: 38405.22, close: 38508.44, volume: 543012345 },
        { date: '2024-01-19', open: 38495.55, high: 38598.88, low: 38465.33, close: 38568.77, volume: 565234567 },
        { date: '2024-01-22', open: 38555.22, high: 38658.44, low: 38525.66, close: 38638.11, volume: 587456789 },
        { date: '2024-01-23', open: 38625.33, high: 38728.55, low: 38595.11, close: 38708.33, volume: 609678901 },
        { date: '2024-01-24', open: 38695.11, high: 38798.44, low: 38665.22, close: 38778.44, volume: 631890123 },
        { date: '2024-01-25', open: 38765.55, high: 38868.88, low: 38735.33, close: 38848.77, volume: 654012345 },
        { date: '2024-01-26', open: 38835.22, high: 38938.44, low: 38805.66, close: 38918.11, volume: 642234567 },
        { date: '2024-01-29', open: 38905.33, high: 39008.55, low: 38875.11, close: 38988.33, volume: 664456789 },
        { date: '2024-01-30', open: 38975.11, high: 39078.44, low: 38945.22, close: 39058.44, volume: 686678901 },
        { date: '2024-01-31', open: 39045.55, high: 39148.88, low: 39015.33, close: 39128.66, volume: 708890123 },
        { date: '2024-02-01', open: 39115.22, high: 39218.44, low: 39085.66, close: 39198.33, volume: 731012345 },
        { date: '2024-02-02', open: 39185.33, high: 39288.55, low: 39155.11, close: 39268.77, volume: 753234567 },
        { date: '2024-02-05', open: 39155.11, high: 39235.44, low: 39125.22, close: 39185.22, volume: 775456789 },
        { date: '2024-02-06', open: 39175.55, high: 39265.88, low: 39145.33, close: 39235.66, volume: 797678901 },
        { date: '2024-02-07', open: 39225.22, high: 39325.44, low: 39195.11, close: 39295.33, volume: 819890123 },
        { date: '2024-02-08', open: 39285.33, high: 39385.55, low: 39255.22, close: 39355.77, volume: 842012345 },
        { date: '2024-02-19', open: 39345.11, high: 39445.44, low: 39315.33, close: 39415.33, volume: 864234567 },
        { date: '2024-02-20', open: 39405.44, high: 39505.88, low: 39375.22, close: 39475.55, volume: 886456789 }
      ],
      latest: { price: 39475.55, change: 60.22, changePercent: 0.15 },
      ma5: 39415.22,
      ma20: 39245.66,
      rsi: 61.2,
      macd: { dif: 85.33, dea: 62.44, macd: 45.78 }
    },
    {
      code: 'IXIC',
      name: '纳斯达克',
      currency: 'USD',
      data: [
        { date: '2024-01-02', open: 15011.34, high: 15058.22, low: 14985.66, close: 15035.55, volume: 456789012 },
        { date: '2024-01-03', open: 15025.11, high: 15098.44, low: 14998.22, close: 15078.33, volume: 478901234 },
        { date: '2024-01-04', open: 15065.33, high: 15138.88, low: 15035.11, close: 15125.22, volume: 501012345 },
        { date: '2024-01-05', open: 15112.22, high: 15185.44, low: 15085.66, close: 15165.55, volume: 523123456 },
        { date: '2024-01-08', open: 15152.11, high: 15225.22, low: 15125.33, close: 15205.66, volume: 545234567 },
        { date: '2024-01-09', open: 15192.55, high: 15268.44, low: 15165.22, close: 15248.33, volume: 567345678 },
        { date: '2024-01-10', open: 15235.22, high: 15312.88, low: 15205.11, close: 15295.77, volume: 589456789 },
        { date: '2024-01-11', open: 15282.33, high: 15358.55, low: 15255.66, close: 15342.11, volume: 611567890 },
        { date: '2024-01-12', open: 15328.11, high: 15398.44, low: 15298.22, close: 15368.44, volume: 599678901 },
        { date: '2024-01-15', open: 15358.55, high: 15438.88, low: 15328.33, close: 15418.66, volume: 621789012 },
        { date: '2024-01-16', open: 15408.22, high: 15488.44, low: 15378.66, close: 15468.33, volume: 643890123 },
        { date: '2024-01-17', open: 15455.33, high: 15528.55, low: 15425.11, close: 15515.77, volume: 665901234 },
        { date: '2024-01-18', open: 15505.11, high: 15578.44, low: 15475.22, close: 15558.44, volume: 654012345 },
        { date: '2024-01-19', open: 15548.55, high: 15618.88, low: 15518.33, close: 15605.77, volume: 676123456 },
        { date: '2024-01-22', open: 15595.22, high: 15668.44, low: 15565.66, close: 15652.11, volume: 698234567 },
        { date: '2024-01-23', open: 15642.33, high: 15718.55, low: 15615.11, close: 15702.33, volume: 720345678 },
        { date: '2024-01-24', open: 15692.11, high: 15768.44, low: 15665.22, close: 15748.44, volume: 742456789 },
        { date: '2024-01-25', open: 15738.55, high: 15818.88, low: 15708.33, close: 15798.77, volume: 764567890 },
        { date: '2024-01-26', open: 15785.22, high: 15858.44, low: 15755.66, close: 15842.11, volume: 752678901 },
        { date: '2024-01-29', open: 15832.33, high: 15908.55, low: 15805.11, close: 15892.33, volume: 774789012 },
        { date: '2024-01-30', open: 15882.11, high: 15958.44, low: 15855.22, close: 15942.44, volume: 796890123 },
        { date: '2024-01-31', open: 15932.55, high: 16008.88, low: 15905.33, close: 15992.66, volume: 818901234 },
        { date: '2024-02-01', open: 15982.22, high: 16058.44, low: 15955.66, close: 16042.33, volume: 841012345 },
        { date: '2024-02-02', open: 16032.33, high: 16108.55, low: 16005.11, close: 16092.77, volume: 863123456 },
        { date: '2024-02-05', open: 15998.11, high: 16068.44, low: 15968.22, close: 16015.22, volume: 885234567 },
        { date: '2024-02-06', open: 16008.55, high: 16088.88, low: 15978.33, close: 16048.66, volume: 907345678 },
        { date: '2024-02-07', open: 16038.22, high: 16118.44, low: 16008.11, close: 16088.33, volume: 929456789 },
        { date: '2024-02-08', open: 16078.33, high: 16158.55, low: 16048.22, close: 16138.77, volume: 951567890 },
        { date: '2024-02-19', open: 16118.11, high: 16198.44, low: 16088.33, close: 16188.33, volume: 973678901 },
        { date: '2024-02-20', open: 16168.44, high: 16248.88, low: 16138.22, close: 16238.55, volume: 995789012 }
      ],
      latest: { price: 16238.55, change: 50.22, changePercent: 0.31 },
      ma5: 16188.22,
      ma20: 16025.44,
      rsi: 63.8,
      macd: { dif: 52.33, dea: 38.55, macd: 27.56 }
    },
    {
      code: 'SPX',
      name: '标普500',
      currency: 'USD',
      data: [
        { date: '2024-01-02', open: 4742.83, high: 4755.22, low: 4735.66, close: 4748.55, volume: 2345678901 },
        { date: '2024-01-03', open: 4745.11, high: 4768.44, low: 4738.22, close: 4762.33, volume: 2456789012 },
        { date: '2024-01-04', open: 4758.33, high: 4782.88, low: 4752.11, close: 4775.22, volume: 2567890123 },
        { date: '2024-01-05', open: 4772.22, high: 4795.44, low: 4765.66, close: 4788.55, volume: 2678901234 },
        { date: '2024-01-08', open: 4785.11, high: 4808.22, low: 4778.33, close: 4802.66, volume: 2789012345 },
        { date: '2024-01-09', open: 4798.55, high: 4822.44, low: 4792.22, close: 4815.33, volume: 2890123456 },
        { date: '2024-01-10', open: 4812.22, high: 4835.88, low: 4805.11, close: 4828.77, volume: 3001234567 },
        { date: '2024-01-11', open: 4825.33, high: 4848.55, low: 4818.66, close: 4842.11, volume: 3112345678 },
        { date: '2024-01-12', open: 4838.11, high: 4858.44, low: 4832.22, close: 4852.44, volume: 3056789012 },
        { date: '2024-01-15', open: 4848.55, high: 4872.88, low: 4842.33, close: 4865.66, volume: 3167890123 },
        { date: '2024-01-16', open: 4862.22, high: 4885.44, low: 4855.66, close: 4878.33, volume: 3278901234 },
        { date: '2024-01-17', open: 4875.33, high: 4898.55, low: 4868.11, close: 4892.77, volume: 3389012345 },
        { date: '2024-01-18', open: 4888.11, high: 4912.44, low: 4882.22, close: 4905.44, volume: 3345678901 },
        { date: '2024-01-19', open: 4902.55, high: 4925.88, low: 4895.33, close: 4918.77, volume: 3456789012 },
        { date: '2024-01-22', open: 4915.22, high: 4938.44, low: 4908.66, close: 4932.11, volume: 3567890123 },
        { date: '2024-01-23', open: 4928.33, high: 4952.55, low: 4922.11, close: 4945.33, volume: 3678901234 },
        { date: '2024-01-24', open: 4942.11, high: 4965.44, low: 4935.22, close: 4958.44, volume: 3789012345 },
        { date: '2024-01-25', open: 4955.55, high: 4978.88, low: 4948.33, close: 4972.77, volume: 3890123456 },
        { date: '2024-01-26', open: 4968.22, high: 4992.44, low: 4962.66, close: 4985.11, volume: 3834567890 },
        { date: '2024-01-29', open: 4982.33, high: 5005.55, low: 4975.11, close: 4998.33, volume: 3945678901 },
        { date: '2024-01-30', open: 4995.11, high: 5018.44, low: 4988.22, close: 5012.44, volume: 4056789012 },
        { date: '2024-01-31', open: 5008.55, high: 5032.88, low: 5002.33, close: 5025.66, volume: 4167890123 },
        { date: '2024-02-01', open: 5022.22, high: 5045.44, low: 5015.66, close: 5038.33, volume: 4278901234 },
        { date: '2024-02-02', open: 5035.33, high: 5058.55, low: 5028.11, close: 5052.77, volume: 4389012345 },
        { date: '2024-02-05', open: 5022.11, high: 5042.44, low: 5012.22, close: 5028.22, volume: 4500123456 },
        { date: '2024-02-06', open: 5025.55, high: 5048.88, low: 5018.33, close: 5038.66, volume: 4611234567 },
        { date: '2024-02-07', open: 5035.22, high: 5058.44, low: 5028.11, close: 5052.33, volume: 4722345678 },
        { date: '2024-02-08', open: 5048.33, high: 5072.55, low: 5042.22, close: 5065.77, volume: 4833456789 },
        { date: '2024-02-19', open: 5062.11, high: 5085.44, low: 5055.33, close: 5078.33, volume: 4944567890 },
        { date: '2024-02-20', open: 5075.44, high: 5098.88, low: 5068.22, close: 5092.55, volume: 5055678901 }
      ],
      latest: { price: 5092.55, change: 14.22, changePercent: 0.28 },
      ma5: 5078.22,
      ma20: 5025.44,
      rsi: 62.1,
      macd: { dif: 35.22, dea: 25.11, macd: 20.22 }
    },
    {
      code: 'NI225',
      name: '日经225',
      currency: 'JPY',
      data: [
        { date: '2024-01-02', open: 33464.78, high: 33568.22, low: 33385.66, close: 33515.55, volume: 189012345 },
        { date: '2024-01-03', open: 33502.11, high: 33615.44, low: 33478.22, close: 33585.33, volume: 201234567 },
        { date: '2024-01-04', open: 33572.33, high: 33685.88, low: 33548.11, close: 33655.22, volume: 213456789 },
        { date: '2024-01-05', open: 33642.22, high: 33755.44, low: 33618.66, close: 33725.55, volume: 225678901 },
        { date: '2024-01-08', open: 33712.11, high: 33825.22, low: 33688.33, close: 33795.66, volume: 237890123 },
        { date: '2024-01-09', open: 33782.55, high: 33895.44, low: 33758.22, close: 33865.33, volume: 250012345 },
        { date: '2024-01-10', open: 33852.22, high: 33965.88, low: 33828.11, close: 33935.77, volume: 262234567 },
        { date: '2024-01-11', open: 33922.33, high: 34035.55, low: 33898.66, close: 34005.11, volume: 274456789 },
        { date: '2024-01-12', open: 33992.11, high: 34098.44, low: 33968.22, close: 34065.44, volume: 268890123 },
        { date: '2024-01-15', open: 34052.55, high: 34165.88, low: 34028.33, close: 34135.66, volume: 281012345 },
        { date: '2024-01-16', open: 34122.22, high: 34235.44, low: 34098.66, close: 34205.33, volume: 293234567 },
        { date: '2024-01-17', open: 34192.33, high: 34305.55, low: 34168.11, close: 34275.77, volume: 305456789 },
        { date: '2024-01-18', open: 34262.11, high: 34375.44, low: 34238.22, close: 34335.44, volume: 317678901 },
        { date: '2024-01-19', open: 34322.55, high: 34435.88, low: 34298.33, close: 34405.77, volume: 309890123 },
        { date: '2024-01-22', open: 34392.22, high: 34505.44, low: 34368.66, close: 34475.11, volume: 322012345 },
        { date: '2024-01-23', open: 34462.33, high: 34575.55, low: 34438.11, close: 34545.33, volume: 334234567 },
        { date: '2024-01-24', open: 34532.11, high: 34645.44, low: 34508.22, close: 34615.44, volume: 346456789 },
        { date: '2024-01-25', open: 34602.55, high: 34715.88, low: 34578.33, close: 34685.77, volume: 358678901 },
        { date: '2024-01-26', open: 34672.22, high: 34785.44, low: 34648.66, close: 34755.11, volume: 350890123 },
        { date: '2024-01-29', open: 34742.33, high: 34855.55, low: 34718.11, close: 34825.33, volume: 363012345 },
        { date: '2024-01-30', open: 34812.11, high: 34925.44, low: 34788.22, close: 34895.44, volume: 375234567 },
        { date: '2024-01-31', open: 34882.55, high: 34995.88, low: 34858.33, close: 34965.66, volume: 387456789 },
        { date: '2024-02-01', open: 34952.22, high: 35065.44, low: 34928.66, close: 35035.33, volume: 399678901 },
        { date: '2024-02-02', open: 35022.33, high: 35135.55, low: 34998.11, close: 35105.77, volume: 411890123 },
        { date: '2024-02-05', open: 34988.11, high: 35088.44, low: 34958.22, close: 35025.22, volume: 424012345 },
        { date: '2024-02-06', open: 34998.55, high: 35098.88, low: 34968.33, close: 35058.66, volume: 436234567 },
        { date: '2024-02-07', open: 35028.22, high: 35128.44, low: 34998.11, close: 35098.33, volume: 448456789 },
        { date: '2024-02-08', open: 35068.33, high: 35168.55, low: 35038.22, close: 35138.77, volume: 460678901 },
        { date: '2024-02-19', open: 35108.11, high: 35208.44, low: 35078.33, close: 35178.33, volume: 472890123 },
        { date: '2024-02-20', open: 35148.44, high: 35248.88, low: 35118.22, close: 35218.55, volume: 485012345 }
      ],
      latest: { price: 35218.55, change: 40.22, changePercent: 0.11 },
      ma5: 35178.22,
      ma20: 35025.44,
      rsi: 59.5,
      macd: { dif: 42.33, dea: 28.55, macd: 27.56 }
    },
    {
      code: 'FTSE',
      name: '富时100',
      currency: 'GBP',
      data: [
        { date: '2024-01-02', open: 7733.01, high: 7748.22, low: 7725.66, close: 7740.55, volume: 890123456 },
        { date: '2024-01-03', open: 7738.11, high: 7762.44, low: 7730.22, close: 7755.33, volume: 912345678 },
        { date: '2024-01-04', open: 7752.33, high: 7778.88, low: 7745.11, close: 7772.22, volume: 934567890 },
        { date: '2024-01-05', open: 7768.22, high: 7795.44, low: 7762.66, close: 7785.55, volume: 956789012 },
        { date: '2024-01-08', open: 7782.11, high: 7808.22, low: 7775.33, close: 7798.66, volume: 978901234 },
        { date: '2024-01-09', open: 7795.55, high: 7822.44, low: 7788.22, close: 7815.33, volume: 1000123456 },
        { date: '2024-01-10', open: 7812.22, high: 7838.88, low: 7805.11, close: 7832.77, volume: 1022345678 },
        { date: '2024-01-11', open: 7828.33, high: 7855.55, low: 7822.66, close: 7848.11, volume: 1044567890 },
        { date: '2024-01-12', open: 7845.11, high: 7865.44, low: 7838.22, close: 7858.44, volume: 1038901234 },
        { date: '2024-01-15', open: 7855.55, high: 7878.88, low: 7848.33, close: 7872.66, volume: 1061012345 },
        { date: '2024-01-16', open: 7868.22, high: 7892.44, low: 7862.66, close: 7885.33, volume: 1083234567 },
        { date: '2024-01-17', open: 7882.33, high: 7905.55, low: 7875.11, close: 7898.77, volume: 1105456789 },
        { date: '2024-01-18', open: 7895.11, high: 7918.44, low: 7888.22, close: 7908.44, volume: 1099678901 },
        { date: '2024-01-19', open: 7905.55, high: 7928.88, low: 7898.33, close: 7922.77, volume: 1121890123 },
        { date: '2024-01-22', open: 7918.22, high: 7942.44, low: 7912.66, close: 7935.11, volume: 1144012345 },
        { date: '2024-01-23', open: 7932.33, high: 7955.55, low: 7925.11, close: 7948.33, volume: 1166234567 },
        { date: '2024-01-24', open: 7945.11, high: 7968.44, low: 7938.22, close: 7958.44, volume: 1188456789 },
        { date: '2024-01-25', open: 7958.55, high: 7982.88, low: 7952.33, close: 7972.77, volume: 1210678901 },
        { date: '2024-01-26', open: 7972.22, high: 7995.44, low: 7965.66, close: 7985.11, volume: 1204890123 },
        { date: '2024-01-29', open: 7985.33, high: 8008.55, low: 7978.11, close: 7998.33, volume: 1227012345 },
        { date: '2024-01-30', open: 7998.11, high: 8022.44, low: 7992.22, close: 8012.44, volume: 1249234567 },
        { date: '2024-01-31', open: 8012.55, high: 8035.88, low: 8005.33, close: 8025.66, volume: 1271456789 },
        { date: '2024-02-01', open: 8025.22, high: 8048.44, low: 8018.66, close: 8038.33, volume: 1293678901 },
        { date: '2024-02-02', open: 8038.33, high: 8062.55, low: 8032.11, close: 8052.77, volume: 1315890123 },
        { date: '2024-02-05', open: 8025.11, high: 8048.44, low: 8018.22, close: 8035.22, volume: 1338012345 },
        { date: '2024-02-06', open: 8028.55, high: 8052.88, low: 8022.33, close: 8045.66, volume: 1360234567 },
        { date: '2024-02-07', open: 8038.22, high: 8062.44, low: 8032.11, close: 8055.33, volume: 1382456789 },
        { date: '2024-02-08', open: 8048.33, high: 8072.55, low: 8042.22, close: 8065.77, volume: 1404678901 },
        { date: '2024-02-19', open: 8058.11, high: 8082.44, low: 8052.33, close: 8075.33, volume: 1426890123 },
        { date: '2024-02-20', open: 8068.44, high: 8092.88, low: 8062.22, close: 8085.55, volume: 1449012345 }
      ],
      latest: { price: 8085.55, change: 10.22, changePercent: 0.13 },
      ma5: 8075.22,
      ma20: 8045.44,
      rsi: 58.8,
      macd: { dif: 18.55, dea: 12.33, macd: 12.44 }
    }
  ],
  stocks: [
    {
      code: '1810.HK',
      name: '小米集团',
      currency: 'HKD',
      sector: '科技',
      data: [
        { date: '2024-01-02', open: 14.82, high: 14.98, low: 14.72, close: 14.88, volume: 98765432 },
        { date: '2024-01-03', open: 14.86, high: 15.05, low: 14.78, close: 14.95, volume: 102345678 },
        { date: '2024-01-04', open: 14.92, high: 15.12, low: 14.85, close: 15.08, volume: 105987654 },
        { date: '2024-01-05', open: 15.05, high: 15.18, low: 14.98, close: 15.02, volume: 108765432 },
        { date: '2024-01-08', open: 14.98, high: 15.15, low: 14.92, close: 15.12, volume: 112345678 },
        { date: '2024-01-09', open: 15.10, high: 15.28, low: 15.02, close: 15.22, volume: 115987654 },
        { date: '2024-01-10', open: 15.20, high: 15.35, low: 15.12, close: 15.30, volume: 118765432 },
        { date: '2024-01-11', open: 15.28, high: 15.42, low: 15.18, close: 15.38, volume: 122345678 },
        { date: '2024-01-12', open: 15.35, high: 15.48, low: 15.28, close: 15.42, volume: 119876543 },
        { date: '2024-01-15', open: 15.40, high: 15.55, low: 15.32, close: 15.48, volume: 125432109 },
        { date: '2024-01-16', open: 15.45, high: 15.62, low: 15.38, close: 15.55, volume: 128765432 },
        { date: '2024-01-17', open: 15.52, high: 15.68, low: 15.45, close: 15.62, volume: 131234567 },
        { date: '2024-01-18', open: 15.58, high: 15.72, low: 15.52, close: 15.65, volume: 129876543 },
        { date: '2024-01-19', open: 15.62, high: 15.78, low: 15.55, close: 15.72, volume: 132345678 },
        { date: '2024-01-22', open: 15.68, high: 15.85, low: 15.62, close: 15.78, volume: 135432109 },
        { date: '2024-01-23', open: 15.75, high: 15.92, low: 15.68, close: 15.85, volume: 138765432 },
        { date: '2024-01-24', open: 15.82, high: 15.98, low: 15.75, close: 15.92, volume: 141234567 },
        { date: '2024-01-25', open: 15.88, high: 16.05, low: 15.82, close: 15.98, volume: 144876543 },
        { date: '2024-01-26', open: 15.95, high: 16.12, low: 15.88, close: 16.05, volume: 147654321 },
        { date: '2024-01-29', open: 16.02, high: 16.18, low: 15.95, close: 16.12, volume: 150234567 },
        { date: '2024-01-30', open: 16.08, high: 16.25, low: 16.02, close: 16.18, volume: 153456789 },
        { date: '2024-01-31', open: 16.15, high: 16.32, low: 16.08, close: 16.25, volume: 156789012 },
        { date: '2024-02-01', open: 16.22, high: 16.38, low: 16.15, close: 16.32, volume: 159234567 },
        { date: '2024-02-02', open: 16.28, high: 16.45, low: 16.22, close: 16.38, volume: 162345678 },
        { date: '2024-02-05', open: 16.22, high: 16.35, low: 16.12, close: 16.18, volume: 165432109 },
        { date: '2024-02-06', open: 16.15, high: 16.32, low: 16.08, close: 16.25, volume: 168765432 },
        { date: '2024-02-07', open: 16.22, high: 16.38, low: 16.15, close: 16.32, volume: 171234567 },
        { date: '2024-02-08', open: 16.28, high: 16.45, low: 16.22, close: 16.38, volume: 174876543 },
        { date: '2024-02-19', open: 16.35, high: 16.52, low: 16.28, close: 16.45, volume: 177654321 },
        { date: '2024-02-20', open: 16.42, high: 16.58, low: 16.35, close: 16.52, volume: 180234567 }
      ],
      latest: { price: 16.52, change: 0.07, changePercent: 0.43 },
      high: 16.58,
      low: 16.35,
      volume: 180234567,
      ma5: 16.38,
      ma20: 16.22,
      rsi: 65.2,
      macd: { dif: 0.18, dea: 0.12, macd: 0.12 }
    },
    {
      code: '9992.HK',
      name: '泡泡玛特',
      currency: 'HKD',
      sector: '消费',
      data: [
        { date: '2024-01-02', open: 22.35, high: 22.58, low: 22.18, close: 22.42, volume: 45678901 },
        { date: '2024-01-03', open: 22.40, high: 22.65, low: 22.28, close: 22.55, volume: 47890123 },
        { date: '2024-01-04', open: 22.52, high: 22.78, low: 22.42, close: 22.68, volume: 50123456 },
        { date: '2024-01-05', open: 22.65, high: 22.85, low: 22.52, close: 22.72, volume: 52345678 },
        { date: '2024-01-08', open: 22.68, high: 22.92, low: 22.58, close: 22.85, volume: 54567890 },
        { date: '2024-01-09', open: 22.82, high: 23.05, low: 22.72, close: 22.98, volume: 56789012 },
        { date: '2024-01-10', open: 22.95, high: 23.15, low: 22.85, close: 23.08, volume: 58901234 },
        { date: '2024-01-11', open: 23.05, high: 23.25, low: 22.95, close: 23.18, volume: 61234567 },
        { date: '2024-01-12', open: 23.15, high: 23.32, low: 23.05, close: 23.25, volume: 59876543 },
        { date: '2024-01-15', open: 23.22, high: 23.42, low: 23.12, close: 23.35, volume: 62345678 },
        { date: '2024-01-16', open: 23.32, high: 23.52, low: 23.22, close: 23.45, volume: 64567890 },
        { date: '2024-01-17', open: 23.42, high: 23.62, low: 23.32, close: 23.55, volume: 66789012 },
        { date: '2024-01-18', open: 23.52, high: 23.68, low: 23.42, close: 23.58, volume: 65432109 },
        { date: '2024-01-19', open: 23.55, high: 23.75, low: 23.45, close: 23.65, volume: 67890123 },
        { date: '2024-01-22', open: 23.62, high: 23.82, low: 23.52, close: 23.75, volume: 70123456 },
        { date: '2024-01-23', open: 23.72, high: 23.92, low: 23.62, close: 23.85, volume: 72345678 },
        { date: '2024-01-24', open: 23.82, high: 23.98, low: 23.72, close: 23.92, volume: 74567890 },
        { date: '2024-01-25', open: 23.88, high: 24.08, low: 23.78, close: 23.98, volume: 76789012 },
        { date: '2024-01-26', open: 23.95, high: 24.15, low: 23.85, close: 24.05, volume: 78901234 },
        { date: '2024-01-29', open: 24.02, high: 24.22, low: 23.92, close: 24.12, volume: 81234567 },
        { date: '2024-01-30', open: 24.08, high: 24.28, low: 23.98, close: 24.18, volume: 83456789 },
        { date: '2024-01-31', open: 24.15, high: 24.35, low: 24.05, close: 24.25, volume: 85678901 },
        { date: '2024-02-01', open: 24.22, high: 24.38, low: 24.12, close: 24.32, volume: 87890123 },
        { date: '2024-02-02', open: 24.28, high: 24.45, low: 24.18, close: 24.38, volume: 89012345 },
        { date: '2024-02-05', open: 24.18, high: 24.32, low: 24.05, close: 24.12, volume: 91234567 },
        { date: '2024-02-06', open: 24.08, high: 24.28, low: 23.98, close: 24.18, volume: 93456789 },
        { date: '2024-02-07', open: 24.15, high: 24.35, low: 24.08, close: 24.25, volume: 95678901 },
        { date: '2024-02-08', open: 24.22, high: 24.42, low: 24.15, close: 24.32, volume: 97890123 },
        { date: '2024-02-19', open: 24.28, high: 24.48, low: 24.18, close: 24.38, volume: 100123456 },
        { date: '2024-02-20', open: 24.35, high: 24.55, low: 24.25, close: 24.45, volume: 102345678 }
      ],
      latest: { price: 24.45, change: 0.07, changePercent: 0.29 },
      high: 24.55,
      low: 24.25,
      volume: 102345678,
      ma5: 24.32,
      ma20: 24.18,
      rsi: 61.8,
      macd: { dif: 0.15, dea: 0.10, macd: 0.10 }
    },
    {
      code: '000660.KS',
      name: 'SK Hynix',
      currency: 'KRW',
      sector: '半导体',
      data: [
        { date: '2024-01-02', open: 138500, high: 139800, low: 137800, close: 139200, volume: 23456789 },
        { date: '2024-01-03', open: 139000, high: 140500, low: 138200, close: 139800, volume: 25678901 },
        { date: '2024-01-04', open: 139600, high: 141200, low: 139000, close: 140800, volume: 27890123 },
        { date: '2024-01-05', open: 140500, high: 141800, low: 139800, close: 141200, volume: 29012345 },
        { date: '2024-01-08', open: 141000, high: 142500, low: 140200, close: 142200, volume: 31234567 },
        { date: '2024-01-09', open: 142000, high: 143500, low: 141200, close: 143200, volume: 33456789 },
        { date: '2024-01-10', open: 143000, high: 144200, low: 142200, close: 143800, volume: 35678901 },
        { date: '2024-01-11', open: 143600, high: 144800, low: 142800, close: 144200, volume: 37890123 },
        { date: '2024-01-12', open: 144000, high: 145200, low: 143200, close: 144800, volume: 36543210 },
        { date: '2024-01-15', open: 144600, high: 145800, low: 143800, close: 145200, volume: 38765432 },
        { date: '2024-01-16', open: 145000, high: 146200, low: 144200, close: 145800, volume: 40987654 },
        { date: '2024-01-17', open: 145600, high: 146800, low: 144800, close: 146200, volume: 43209876 },
        { date: '2024-01-18', open: 146000, high: 147200, low: 145200, close: 146800, volume: 41876543 },
        { date: '2024-01-19', open: 146600, high: 147800, low: 145800, close: 147200, volume: 44098765 },
        { date: '2024-01-22', open: 147000, high: 148200, low: 146200, close: 147800, volume: 46321098 },
        { date: '2024-01-23', open: 147600, high: 148800, low: 146800, close: 148200, volume: 48543210 },
        { date: '2024-01-24', open: 148000, high: 149200, low: 147200, close: 148800, volume: 50765432 },
        { date: '2024-01-25', open: 148600, high: 149800, low: 147800, close: 149200, volume: 52987654 },
        { date: '2024-01-26', open: 149000, high: 150200, low: 148200, close: 149800, volume: 51654321 },
        { date: '2024-01-29', open: 149600, high: 150800, low: 148800, close: 150200, volume: 53876543 },
        { date: '2024-01-30', open: 150000, high: 151200, low: 149200, close: 150800, volume: 56098765 },
        { date: '2024-01-31', open: 150600, high: 151800, low: 149800, close: 151200, volume: 58321098 },
        { date: '2024-02-01', open: 151000, high: 152200, low: 150200, close: 151800, volume: 60543210 },
        { date: '2024-02-02', open: 151600, high: 152800, low: 150800, close: 152200, volume: 62765432 },
        { date: '2024-02-05', open: 151200, high: 152200, low: 150200, close: 150800, volume: 64987654 },
        { date: '2024-02-06', open: 150600, high: 151800, low: 149800, close: 151200, volume: 67209876 },
        { date: '2024-02-07', open: 151000, high: 152200, low: 150200, close: 151800, volume: 69432109 },
        { date: '2024-02-08', open: 151600, high: 152800, low: 150800, close: 152200, volume: 71654321 },
        { date: '2024-02-19', open: 152000, high: 153200, low: 151200, close: 152800, volume: 73876543 },
        { date: '2024-02-20', open: 152600, high: 153800, low: 151800, close: 153200, volume: 76098765 }
      ],
      latest: { price: 153200, change: 600, changePercent: 0.39 },
      high: 153800,
      low: 151800,
      volume: 76098765,
      ma5: 152200,
      ma20: 151200,
      rsi: 64.5,
      macd: { dif: 2800, dea: 1800, macd: 2000 }
    }
  ],
  news: [
    {
      id: 1,
      title: '港股三大指数集体上涨，恒生科技指数涨超2%',
      summary: '受外围市场走强及南向资金持续流入影响，港股三大指数今日集体上涨，恒生科技指数表现亮眼，涨超2%。',
      source: '财联社',
      time: '2024-02-20 16:30',
      category: '港股',
      url: '#'
    },
    {
      id: 2,
      title: 'A股三大指数收涨，北向资金净买入超50亿元',
      summary: '沪深两市今日震荡上行，沪指收涨0.32%，北向资金大幅净买入，市场情绪有所回暖。',
      source: '新浪财经',
      time: '2024-02-20 15:05',
      category: 'A股',
      url: '#'
    },
    {
      id: 3,
      title: '美联储会议纪要释放鸽派信号，美股三大指数齐涨',
      summary: '美联储最新会议纪要显示，多数委员认为加息周期已结束，美股三大指数应声上涨，纳指涨超1%。',
      source: '华尔街见闻',
      time: '2024-02-20 09:15',
      category: '美股',
      url: '#'
    },
    {
      id: 4,
      title: '小米汽车SU7正式发布，股价创年内新高',
      summary: '小米集团首款电动汽车SU7正式发布，售价21.59万元起，受此利好消息提振，小米股价今日创年内新高。',
      source: '第一财经',
      time: '2024-02-20 14:20',
      category: '科技股',
      url: '#'
    },
    {
      id: 5,
      title: 'SK海力士Q4业绩超预期，HBM芯片需求强劲',
      summary: '韩国存储芯片巨头SK海力士发布2023年第四季度财报，营收和利润均超市场预期，HBM高带宽内存芯片需求持续强劲。',
      source: '路透社',
      time: '2024-02-20 08:45',
      category: '科技股',
      url: '#'
    },
    {
      id: 6,
      title: '中国1月CPI同比上涨0.8%，PPI同比下降2.5%',
      summary: '国家统计局公布数据显示，1月CPI同比上涨0.8%，PPI同比下降2.5%，通胀数据温和，市场关注后续政策走向。',
      source: '新华社',
      time: '2024-02-20 10:00',
      category: '宏观经济',
      url: '#'
    },
    {
      id: 7,
      title: '泡泡玛特海外业务增长强劲，东南亚市场成新增长点',
      summary: '泡泡玛特公布2023年业绩预告，海外业务收入同比增长超100%，东南亚市场表现尤为突出，成为公司新的增长引擎。',
      source: '证券时报',
      time: '2024-02-20 11:30',
      category: '消费股',
      url: '#'
    },
    {
      id: 8,
      title: '日本央行维持超宽松货币政策，日元汇率承压',
      summary: '日本央行宣布维持现行政策利率不变，继续实施量化质化宽松政策，日元兑美元汇率应声下跌，市场预期日银短期难转向。',
      source: '日本经济新闻',
      time: '2024-02-20 12:00',
      category: '宏观经济',
      url: '#'
    }
  ],
  lastUpdate: '2024-02-20 16:45:00'
};

function createMiniChart(canvasId, data, isPositive) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const width = canvas.width;
  const height = canvas.height;

  const prices = data.map(d => d.close);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const priceRange = maxPrice - minPrice || 1;

  const lineColor = isPositive ? '#ef4444' : '#22c55e';
  const gradientStart = isPositive ? 'rgba(239, 68, 68, 0.3)' : 'rgba(34, 197, 94, 0.3)';
  const gradientEnd = isPositive ? 'rgba(239, 68, 68, 0)' : 'rgba(34, 197, 94, 0)';

  ctx.clearRect(0, 0, width, height);

  const gradient = ctx.createLinearGradient(0, 0, 0, height);
  gradient.addColorStop(0, gradientStart);
  gradient.addColorStop(1, gradientEnd);

  ctx.beginPath();
  ctx.moveTo(0, height - ((prices[0] - minPrice) / priceRange) * height);

  for (let i = 1; i < prices.length; i++) {
    const x = (i / (prices.length - 1)) * width;
    const y = height - ((prices[i] - minPrice) / priceRange) * height;
    ctx.lineTo(x, y);
  }

  ctx.strokeStyle = lineColor;
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.lineTo(width, height);
  ctx.lineTo(0, height);
  ctx.closePath();
  ctx.fillStyle = gradient;
  ctx.fill();
}

function renderIndices() {
  const container = document.getElementById('indices-container');
  if (!container) return;

  container.innerHTML = marketData.indices.map((index, idx) => {
    const isPositive = index.latest.change >= 0;
    const changeSign = isPositive ? '+' : '';
    const changeClass = isPositive ? 'text-red-500' : 'text-green-500';
    const canvasId = `chart-index-${idx}`;

    return `
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between mb-2">
          <div>
            <h3 class="font-semibold text-gray-800">${index.name}</h3>
            <p class="text-xs text-gray-500">${index.code}</p>
          </div>
          <span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">${index.currency}</span>
        </div>
        <div class="mb-3">
          <p class="text-xl font-bold text-gray-900">${index.latest.price.toLocaleString()}</p>
          <p class="${changeClass} text-sm font-medium">
            ${changeSign}${index.latest.change.toFixed(2)} (${changeSign}${index.latest.changePercent.toFixed(2)}%)
          </p>
        </div>
        <canvas id="${canvasId}" width="200" height="60" class="w-full"></canvas>
        <div class="flex justify-between text-xs text-gray-500 mt-2">
          <span>MA5: ${index.ma5.toFixed(2)}</span>
          <span>MA20: ${index.ma20.toFixed(2)}</span>
          <span>RSI: ${index.rsi.toFixed(1)}</span>
        </div>
      </div>
    `;
  }).join('');

  setTimeout(() => {
    marketData.indices.forEach((index, idx) => {
      createMiniChart(`chart-index-${idx}`, index.data, index.latest.change >= 0);
    });
  }, 0);
}

function renderStocks() {
  const container = document.getElementById('stocks-container');
  if (!container) return;

  container.innerHTML = marketData.stocks.map((stock, idx) => {
    const isPositive = stock.latest.change >= 0;
    const changeSign = isPositive ? '+' : '';
    const changeClass = isPositive ? 'text-red-500' : 'text-green-500';
    const canvasId = `chart-stock-${idx}`;

    const volumeStr = stock.volume >= 100000000
      ? (stock.volume / 100000000).toFixed(2) + '亿'
      : stock.volume >= 10000
        ? (stock.volume / 10000).toFixed(2) + '万'
        : stock.volume.toLocaleString();

    return `
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between mb-2">
          <div>
            <h3 class="font-semibold text-gray-800">${stock.name}</h3>
            <p class="text-xs text-gray-500">${stock.code}</p>
          </div>
          <span class="text-xs px-2 py-1 rounded-full bg-blue-50 text-blue-600">${stock.sector}</span>
        </div>
        <div class="mb-3">
          <p class="text-xl font-bold text-gray-900">${stock.latest.price.toLocaleString()} ${stock.currency}</p>
          <p class="${changeClass} text-sm font-medium">
            ${changeSign}${stock.latest.change.toFixed(2)} (${changeSign}${stock.latest.changePercent.toFixed(2)}%)
          </p>
        </div>
        <canvas id="${canvasId}" width="200" height="60" class="w-full"></canvas>
        <div class="grid grid-cols-2 gap-2 text-xs text-gray-600 mt-2">
          <div class="flex justify-between">
            <span class="text-gray-500">最高</span>
            <span>${stock.high.toLocaleString()}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">最低</span>
            <span>${stock.low.toLocaleString()}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">成交量</span>
            <span>${volumeStr}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">RSI</span>
            <span>${stock.rsi.toFixed(1)}</span>
          </div>
        </div>
        <div class="flex justify-between text-xs text-gray-500 mt-2 pt-2 border-t border-gray-100">
          <span>MA5: ${stock.ma5.toFixed(2)}</span>
          <span>MA20: ${stock.ma20.toFixed(2)}</span>
        </div>
      </div>
    `;
  }).join('');

  setTimeout(() => {
    marketData.stocks.forEach((stock, idx) => {
      createMiniChart(`chart-stock-${idx}`, stock.data, stock.latest.change >= 0);
    });
  }, 0);
}

function renderNews() {
  const container = document.getElementById('news-container');
  if (!container) return;

  container.innerHTML = marketData.news.map(news => {
    const categoryColors = {
      '港股': 'bg-orange-50 text-orange-600',
      'A股': 'bg-red-50 text-red-600',
      '美股': 'bg-blue-50 text-blue-600',
      '科技股': 'bg-purple-50 text-purple-600',
      '消费股': 'bg-pink-50 text-pink-600',
      '宏观经济': 'bg-gray-100 text-gray-600'
    };
    const categoryClass = categoryColors[news.category] || 'bg-gray-100 text-gray-600';

    return `
      <a href="${news.url}" class="block p-4 bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all hover:border-blue-200">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-xs px-2 py-0.5 rounded-full ${categoryClass}">${news.category}</span>
          <span class="text-xs text-gray-400">${news.time}</span>
        </div>
        <h4 class="font-medium text-gray-800 mb-2 line-clamp-2 hover:text-blue-600">${news.title}</h4>
        <p class="text-sm text-gray-500 line-clamp-2">${news.summary}</p>
        <div class="flex items-center gap-1 mt-3 text-xs text-gray-400">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
          </svg>
          <span>${news.source}</span>
        </div>
      </a>
    `;
  }).join('');
}

function updateLastUpdate() {
  const element = document.getElementById('last-update');
  if (element) {
    element.textContent = `最后更新: ${marketData.lastUpdate}`;
  }
}

function initDashboard() {
  renderIndices();
  renderStocks();
  renderNews();
  updateLastUpdate();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboard);
} else {
  initDashboard();
}

window.marketData = marketData;
window.renderIndices = renderIndices;
window.renderStocks = renderStocks;
window.renderNews = renderNews;
window.initDashboard = initDashboard;
