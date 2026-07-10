# Risk-Off Shocks and Spillovers in Safe Havens

> Beirne, J. and E. Sugandi (2022/2023)

ADBI Working Paper Series




RISK-OFF SHOCKS AND SPILLOVERS
IN SAFE HAVENS




John Beirne and Eric Sugandi




No. 1345
November 2022




Asian Development Bank Institute
 John Beirne is Vice-Chair of Research and Senior Research Fellow, and Eric Sugandi is
 a Project Consultant, both at the Asian Development Bank Institute.
 The views expressed in this paper are the views of the author and do not necessarily
 reflect the views or policies of ADBI, ADB, its Board of Directors, or the governments
 they represent. ADBI does not guarantee the accuracy of the data included in this paper
 and accepts no responsibility for any consequences of their use. Terminology used may
 not necessarily be consistent with ADB official terms.
 Discussion papers are subject to formal revision and correction before they are finalized
 and considered published.


The Working Paper series is a continuation of the formerly named Discussion Paper series;
the numbering of the papers continued without interruption or change. ADBI’s working
papers reflect initial ideas on a topic and are posted online for discussion. Some working
papers may develop into other forms of publication.


Suggested citation:

Beirne, J. and E. Sugandi. 2022. Risk-off Shocks and Spillovers in Safe Havens. ADBI
Working Paper 1345. Tokyo: Asian Development Bank Institute. Available:
https://doi.org/10.56506/GUUX7790

Please contact the authors for information about this paper.

Email: jbeirne@adbi.org, esugandi@adbi.org

 We are grateful for comments received on the paper at the Japan Finance
 Association/PBFJ conference at Kyushu University, Japan on 14–15 March 2022.




Asian Development Bank Institute
Kasumigaseki Building, 8th Floor
3-2-5 Kasumigaseki, Chiyoda-ku
Tokyo 100-6008, Japan

Tel:      +81-3-3593-5500
Fax:      +81-3-3593-5571
URL:      www.adbi.org
E-mail:   info@adbi.org

© 2022 Asian Development Bank Institute
ADBI Working Paper 1345                                                    Beirne and Sugandi


Abstract

This paper examines real and financial spillovers to safe haven financial flow destinations
due to risk-off shocks in global financial markets. Using country-specific structural vector
autoregression (VAR) models over the period 1990 to 2021, we show that dynamics for
Japan appear to be different to those of Switzerland and the US in four main ways. First, in
response to risk-off episodes over the estimation period, the yen real effective exchange rate
(REER) appreciates sharply and significantly, with the effect persisting over time. Second,
no significant effects on portfolio flows to Japan are found, in spite of the exchange rate
effects, suggesting a rapid adjustment of financial markets to shifts in equilibrium exchange
rates. Third, negative real spillovers from risk-off shocks appear to only apply to Japan with
exchange rate appreciation exacerbating declines in GDP growth. Fourth, risk-off shocks do
not have a statistically significant effect on domestic economic policy uncertainty in Japan,
which may be related to the strong expectations priced in of overseas portfolio holdings
repatriated back to Japan. Our findings have important implications for policymakers in safe
haven destinations in managing domestic financial vulnerabilities associated with risk-off
episodes.

Keywords: risk-off episodes, safe haven assets, economic policy uncertainty

JEL Classification: F32, F41, F62
ADBI Working Paper 1345                                                                                  Beirne and Sugandi



Contents

1.        INTRODUCTION ..........................................................................................................1

2.        RELATED LITERATURE .............................................................................................2

3.        STYLIZED FACTS ON RISK-OFF EPISODES IN SAFE HAVEN
          FINANCIAL MARKETS ................................................................................................4

4.        DATA AND EMPIRICAL METHODOLOGY .................................................................9

5.        EMPIRICAL RESULTS ..............................................................................................10

6.        CONCLUSIONS .........................................................................................................15

REFERENCES ......................................................................................................................16

APPENDIXES

          1         Financial Markets and Risk-off Events in Japan ............................................19
          2         Responses to Risk-off Shocks: Restricted VAR Models ................................23
          3         Responses to Risk-off Shocks: Unrestricted VAR Models .............................26
          4         Daily, Weekly, and Monthly Impulse Response Functions (IRFs)
                    of the Restricted VAR Models ........................................................................29
ADBI Working Paper 1345                                               Beirne and Sugandi




1. INTRODUCTION
During periods of heightened financial stress or for portfolio diversification, global
investors place funds in “safe haven” and “hedge” assets. Baur and Lucey (2010)
define a “hedge” security as a security that is uncorrelated with stocks or bonds on
average, while a “safe haven” security is a security that is uncorrelated with stocks and
bonds in a market crash. Hossfeld and MacDonald (2014) refine Baur and Lucey’s
definitions for a “safe haven” currency and a “hedge” currency. They define a safe
haven currency as a currency whose effective returns are negatively related to global
stock market returns in times of high financial stress, while a hedge currency is a
currency whose effective returns are negatively related to global stock market returns
on average (i.e., unconditional on the stress-regime).
Many investors have long perceived Japanese financial assets (including the Japanese
government bonds (JGBs) and stocks) and the Japanese Yen (JPY) as safe-haven
instruments. JGBs and the JPY are highly related because investors buy (sell) the JPY
when they purchase (sell) the JPY-denominated JGBs. Japanese financial assets and
the JPY have notable negative correlations with the global stock and bond market
returns during global financial crises. Foreign investors bought Japanese assets and
the JPY during crises, such as the 2001 dot.com crisis and the 2007/08 – 2008 Global
Financial Crisis. Some studies point out Japan’s net surplus in its international
investment position and monetary policy sovereignty are the main reasons behind
Japanese financial assets and the JPY’s safe haven status. While safe havens offer
investors a hedge during periods of crisis, domestic currency appreciations can worsen
competitiveness, negatively affecting the domestic stock market, with subsequent
negative wealth effects. With a focus on Japan, also making comparisons to two other
key safe haven destinations, namely Switzerland and the US, this paper aims to
empirically examine real and financial spillovers due to risk-off shocks in financial
markets.
Country-specific structural vector autoregression (VAR) models are estimated over the
period 1990 to 2021 to identify the response of domestic output, policy uncertainty,
financial markets, and capital flows in safe havens to risk-off shocks. Overall, we find
that Japan responds differently in four main ways. First, in response to risk-off
episodes, the yen real effective exchange rate (REER) appreciates sharply and
significantly, with the effect persisting over time. Second, no significant effect on
portfolio flows to Japan are found, in spite of the appreciating exchange rate effect,
suggesting a rapid adjustment of financial markets to shifts in equilibrium exchange
rates. Third, negative real spillovers from risk-off shocks appear to only apply to Japan
with exchange rate appreciation exacerbating declines in GDP growth. Fourth, we find
that risk-off shocks do not have a statistically significant effect on domestic economic
policy uncertainty in Japan, which may be related to the strong expectations priced in
of overseas portfolio holdings repatriated back to Japan. We offer implications for
policy makers based on these findings, aimed mainly at addressing risks to domestic
financial stability that result from risk-off shocks. The remainder of the paper is
organized as follows: Section 2 reviews the related literature on safe haven currencies
and assets. Section 3 explores the stylized facts on risk-off episodes in in safe haven
financial markets. Section 4 describes the data and methodology. Section 5 analyzes
the empirical results. Section 6 concludes.




                                           1
ADBI Working Paper 1345                                                 Beirne and Sugandi




2. RELATED LITERATURE
This paper contributes to the literature on safe haven financial flows. During periods
of heightened financial stress, it is well documented that investors re-balance their
assets towards so-called safe haven currencies, which are low-yielding currencies that
appreciate in times of higher global financial uncertainty (e.g., Habib and Stracca
2012). Traditionally, the US dollar (USD), the Japanese yen (JPY) and the Swiss franc
(CHF) are considered safe haven currencies, with Todorova (2020) noting that global
investors tend to place their funds in the JPY and the CHF whenever uncertainty arises
in the US stock markets or the USD weakens (see also Botman, De Carvalho Filho,
and Lam 2013; Ranaldo and Söderlind 2010; De Bock and De Carvalho Filho 2013;
Masujima 2017; and Balcilara et al. 2020).
Among the safe haven currencies, Cho and Han (2021) observed that the yen, euro
and Swiss franc are more likely to appreciate in periods of high volatility in foreign
exchange markets and rising US Treasury bond yields. In addition, it is noted that the
decline in US stock returns is related only to yen appreciation. According to Fatum and
Yamamoto (2015), the yen appreciates as market uncertainty increases regardless of
the prevailing level of uncertainty whereas all other bilateral USD rates display a
nonlinear pattern. They find that the JPY is the “safest” of safe haven currencies and
that only the JPY has appreciated when market uncertainty increased. The CHF and
the USD are the “second safest” and “third safest”, respectively. When uncertainty
rises, the CHF appreciates significantly against all other currencies but the JPY, while
the USD appreciates significantly against all but the JPY and the CHF.
Safe haven currencies tend to be associated with three key factors: low interest rates
(carry-trade opportunity); large net foreign asset positions; and highly liquid financial
markets. Indeed, Habib and Stracca (2012) stress the feature of net foreign asset
positions, which (after controlling for carry trade) is the most consistent and robust
predictor of a safe haven status, as well as being a key indicator of country risk and
external vulnerability. Other important factors characterizing safe havens include their
level of financial development and the depth of liquidity in the foreign exchange market.
In addition, for currencies that are subject to carry trade, the interest rate spread
relative to the US is significant for advanced countries. Confirming that the unwinding
of carry trade causes the yen to appreciate against the dollar, Nishigaki (2007) finds
that the US stock price has a dominant impact on yen carry trade. The study also
indicates that the interest rate differential between Japan and the US and the interest
rate adjustment by the Bank of Japan (BOJ) does not influence carry trade activity.
Related to this, Imakubo, Kamada, and Kan (2015) discuss the “currency premium”
(i.e., the expected excess return on that currency) that determines the demand for safe
haven currencies. In their model, the currency premium consists of two disequilibrium
factors: (i) the interest rate gap (i.e., the deviation of real interest rates, domestic and
foreign, from their equilibrium values; and (ii) the exchange rate misalignment (i.e., the
deviation of real exchange rates from their equilibrium values).
Min, McDonald, and Shin (2016) relate a “safe haven” status to negative dynamic
conditional correlations (DCCs) between equities and currencies, with currency returns
negatively correlated with stock returns in safe haven countries. They also found that
stock and foreign exchange volatility indexes increase DCCs for countries without safe
assets, while the opposite is found for countries with safe assets, i.e., reducing DCCs.
Moreover, higher country-specific risk, as measured by the US Treasury-Euro Dollar
(TED) spread and credit default swap (CDS) spread, means higher DCCs, a feature of
economies without safe haven status. More recently, Habib, Stracca, and Venditti
(2020) noted that inertia (whether the bond behaved as a safe asset in the past)


                                             2
ADBI Working Paper 1345                                                 Beirne and Sugandi



and good institutions foster a safe asset status, while the size of the debt market is also
significant, reflecting the special role of the US. There are also differences depending
on the level of economic development; the political risk rating and the size of the debt
market are found to be important for advanced countries only, while inertia, real GDP,
and external sustainability (measured by the current account) are important for
emerging markets only.
Hossfeld and MacDonald (2014) identify the safe haven currencies among the G10
countries (i.e., the AUD, CAD, CHF, EUR, JPY, NOK, NZD, SEK, GBP, and USD) by
making a distinction between the “safe haven” flows (i.e., capital movements by
investors who believe that a particular currency area is a relatively safe place to invest)
and the unwinding of currency carry trades (i.e., speculative transactions where
investors seek to take advantage of interest rate differentials to generate superior
returns) during a crisis. They find that the CHF and USD are safe haven currencies.
The JPY appreciation in times of crisis is mainly attributable to the unwinding of the
carry trades rather than caused by the “safe haven” inflows. Meanwhile, the EUR does
not show any crisis-specific reaction. Grisse and Nitschka (2015) note that the yen is a
better hedge than the Swiss franc because of the limited asset market size and liquidity
of the Swiss franc. Beckmann and Czudaj (2016) find that the yen is exceptional in
two ways: expectation errors decrease with higher uncertainty, especially for monetary
policy uncertainty; the yen is the only currency to appreciate in case of higher
uncertainty. Rogoff and Tashiro (2015) discuss the “exorbitant” privilege of the JPY due
to the country’s ability to borrow from abroad at lower rates than other countries, as
well as being able to attain a cost advantage in any kind of borrowing or investment
instrument in a broader sense. This is similar to the US experience in the post-war
period.
Botman, De Carvalho Filho, and Lam (2013) point out the driver of yen risk-off
appreciation appears to be unrelated to capital inflows (cross-border transactions) and
also not linked to expectations about the relative stance of global monetary policies.
Instead, they show that portfolio rebalancing through offshore derivative transactions
occur contemporaneously to yen risk-off appreciations. In particular, they find that the
JPY on average appreciates against the USD during the risk-off episodes in the global
financial market. They find that capital inflows or expectations of the future monetary
policy stance cannot explain the safe haven behavior of the JPY. Instead, changes in
market participants’ risk perceptions trigger derivatives trading, which leads to changes
in the spot exchange rate without capital flows. Specifically, the risk-off episodes
coincide with the forward hedging and reduced net short positions or a buildup of net
long positions in the JPY. On the relationship between monetary policy and safe haven
status, Beckmann and Czudaj (2017) argue that monetary policy is a substantial driver
for exchange rate expectations and unconventional monetary policy has strong
spillover effects across borders, leading to an unexpected safe haven status of the US
dollar after 2008 crisis. Moreover, noting that the appreciation of safe haven currency
is resilient to the changes in monetary policy, Jäggi, Schlegel, and Zanetti (2019) find
that the Japanese yen and Swiss franc respond nonlinearly, depending 0n the direction
of the effect on the exchange rate, with a stronger reaction to surprises generating
an appreciation compared to surprises leading to depreciation. Additionally, both
currencies also systematically respond to changes in the general market environment.
On Japan, Masujima (2017) suggests that while the yen’s strength is driven by its safe
haven status, this may slow down the post-crisis recovery via net exports. In addition,
large-scale monetary easing as a policy response may mask financial vulnerabilities
related to the sustainability of the public finances. However, Iwaisako and Nakata
(2017) warn that the impact of yen appreciation on export fluctuations should not be


                                            3
ADBI Working Paper 1345                                                 Beirne and Sugandi



exaggerated, noting that aggregate global demand played a more important role in the
trade decline after the 2008 crisis. A more recent study by Belke and Volz (2020)
provided insights on how yen appreciation contributed to the structural change of the
Japanese economy – the hollowing out of Japanese industry.
Moreover, Dekle (1998) found that the price change induced by exchange rate
fluctuation has sizable long-term effect on the Japanese employment market. In other
work, Lam and Tokuoka (2013) observe that the yields of the Japanese government
bonds (JGBs) have remained low and stable because of steady inflows from the
Japanese household and corporate sector, the high domestic ownership of the JGBs,
and safe haven inflows. That said, there are risks to the JGB markets, including the
decline of private-sector savings (partly due to the aging population) and potential
spillovers from global financial distresses (which can push the JGB yields higher). In
addition, Horioka, Nomoto, and Terada-Hagiwara (2014) notes that while Japan’s
excessive government debt has not resulted in high economic costs in the past
because of the country’s robust domestic savings, it may lead to substantial costs in
the future as domestic savings decline (as a result of population aging) and due to the
temporary nature of foreign capital inflows to Japanese government securities.
The literature overall highlights the negative impact on the domestic economy due to a
safe haven status. Habib, Stracca and Venditti (2020) note that the high demand for
safe assets in crisis times can lead to a decline in the natural real interest rate, with
adjustment mechanisms disrupted due to exchange rate appreciation and a contraction
in global demand emanating. Transitory real appreciation may create hefty adjustment
costs to the economy, and subsequently, economic dislocation when exchange rates
eventually revert back (e.g., Bussière, Lopez, and Tille 2013). The longer-lasting the
real appreciation and surge in capital flows, the greater the potential for vulnerabilities
to build up in either private or public sector balance sheets. Moreover, in economies
with already low inflation and interest rates close to the zero bound, real appreciations
driven by risk-off episodes could feed deflation risks and place downward pressures on
aggregate demand.
This paper contributes to the prevailing literature by empirically examining real and
financial spillovers in safe haven financial flow destinations in response to risk-off
shocks. Focusing on responses to risk-0ff shocks in output, economic policy
uncertainty, financial markets, and capital flow dynamics, we aim to uncover similarities
and differences across key safe haven destinations in Asia, Europe, and the US. In this
way, we can examine whether the conventional characteristics of safe havens apply in
a uniform manner.


3. STYLIZED FACTS ON RISK-OFF EPISODES
   IN SAFE HAVEN FINANCIAL MARKETS: THE CASE
   OF JAPAN
Prior to discussing the empirical approach and findings, this section presents an
overview of the risk-off episode definition and the basic relation between risk-off
episodes and developments in financial markets of safe havens. We base our
definitions of the risk-off event and episode on a method introduced by De Bock and
De Carvalho Filho (2013), which uses the Chicago Board Options Exchange’s Volatility
Index (i.e., the VIX) as a benchmark. Botman, De Carvalho Filho, and Lam (2013) also
use this method. In this method, a risk-off event occurs when




                                            4
ADBI Working Paper 1345                                                                          Beirne and Sugandi



the VIX is 10 percentage points higher than its 60-day backward-looking moving
average (MA).
Figure 1 displays the VIX movements and the risk-off episodes (i.e., series of risk-off
events) from 1990 to 2021, while Table 1 lists the initial date of those risk-off episodes.
The data sets in those two studies end in 2011, while ours continues until October
2021. We identify six risk-off episodes from 2012 to 2021, including the latest one that
started in February 2020 due to the COVID-19 pandemic outbreak.

                                Figure 1: Risk-off Episodes, 1990–2021




Note: Plotted are fluctuations in the VIX, its 60-day moving average, and our calculated risk-off episodes.
Source: Bloomberg, Authors’ calculation.


The JPY is both a hedge and a safe haven currency. Global investors buy the JPY both
when they seek to hedge their investments during the risk-off episodes. The JPY tends
to appreciate against the USD during the risk-off episodes (Figure 2).1
At the start of the global financial crisis (GFC) in 2007, investors tilted portfolios
towards the yen in search of safety amid prevailing high-risk aversion. The yen
appreciated strongly during this period as a result. This appreciation was bolstered by
the Tōhoku earthquake and tsunami of March 2011 as Japanese investors sold assets
denominated in foreign currency. At the end of 2012, the announcement by new Japan
Prime Minister Shinzo Abe that the Bank of Japan should aggressively increase the
money supply to stimulate inflation (part of the so-called “Abenomics” strategy)
triggered a yen depreciation. Global risk appetite resumed as investors engaged in yen
carry-trade operations, borrowing in the low-yielding yen to fund investment in risky
assets abroad. An equity market shock and slowdown in the People’s Republic of
China (PRC) at the end of 2015 increased global market volatility, leading to yen safe
haven flows, marking the end of the depreciating trend that had been in place since the

1
 The period following the Russian Federation’s invasion of Ukraine on 24 February 2022 coincided with a
sharp depreciation of the yen relative to the US dollar, calling into question the yen’s safe haven status,
which was driven by widening yield differentials between the US and Japan and rising energy prices
worsening Japan’s balance of payments position. Aggressive monetary policy tightening by the US Federal
Reserve to combat inflation, in conjunction with higher global risk aversion, meant that the US dollar
soared during this period at the global level, including against traditional safe haven currencies such as the
yen and Swiss franc.


                                                            5
ADBI Working Paper 1345                                                              Beirne and Sugandi



end of 2012. Since 2017, the yen has been relatively stable, even during the COVID-19
crisis, although a mild appreciation was observed in the first stage of the pandemic,
which later reverted towards the end of 2020 as uncertainty declined. This has
prompted some analysts (e.g., Clynch 2020; Lewis 2020) to suggest that the JPY may
no longer be as attractive as a safe haven as it was in the 2000s. Demand for the JPY
during the risk-off episodes in recent years has been weaker than in two decades ago.
The JPY’s trading range has stabilized below 10%, much lower than in the 2000s
(Clynch 2020).

                                Table 1: Risk-off Episodes Initial Date
                                                                                 Botman,
                                                                               De Carvalho     De Bock and
                                                                                Filho, and     de Carvalho
No.                     Risk-off Event Initial Date              Our Paper     Lam (2013)      Filho (2013)
1      US savings and loans                                      03-Aug-90      03-Aug-90            –
2      Iraq War                                                  14-Jan-91      14-Jan-91            –
3      Escalation of Asian crisis                                29-Oct-97      29-Oct-97        29-Oct-97
4      Concerns on Russian economy                               04-Aug-98      04-Aug-98       04-Aug-98
5      Fear of slowing US economy                                12-Oct-00      12-Oct-00        12-Oct-00
6      9/11 Attacks                                              17-Sep-01      11-Sep-01       17-Sep-01
7      Fear of slowing US economy                                10-Jul-02      10-Jul-02        10-Jul-02
8      Concerns over rising US inflation                         13-Jun-06          –                –
9      BNP Paribas halts withdrawals from three money market     09-Aug-07      10-Aug-07       10-Aug-07
       mutual funds
10     Disruptions in USD money markets                              –          12-Nov-07       12-Nov-07
11     Lehman failure                                            17-Sep-08      17-Sep-08       17-Sep-08
12     Greek crisis                                              06-May-10      06-May-10       06-May-10
13     Uncertainty over impact of Japan’s March 11 earthquake    16-Mar-11      16-Mar-11       16-Mar-11
14     Confrontation over US debt ceiling and deterioration of   04-Aug-11      04-Aug-11       04-Aug-11
       crisis in Euro Area
15     Concerns over deteriorating earning reports (US stock     13-Oct-14          –                –
       markets fall)
16     Thalys train attack, rising tension in Korean Peninsula   21-Aug-15          –                –
17     UK referendum decision: Brexit                            24-Jun-16          –                –
18     Concerns over rising US inflation                         05-Feb-18          –                –
19     Concerns over rapidly rising US interest rates            11-Oct-18          –                –
20     Concerns over COVID-19 outbreak                           24-Feb-20          –                –

Source: Botman, De Carvalho Filho, and Lam (2013), De Bock and De Carvalho Filho (2013), Bloomberg, Authors’
calculation.




                                                           6
ADBI Working Paper 1345                                                                        Beirne and Sugandi



                              Figure 2: USD/JPY and Risk-off Episodes




Note: Plotted are the bilateral nominal USD/JPY exchange rate and our calculated risk-off episodes.
Source: Bloomberg, Authors’ calculation.

Lewis (2020) lists three main reasons behind the underperforming JPY (i.e., it
appreciated less than market players’ expectations): (1) Japan is suffering from trade
deficits; (2) Japanese assets managers continue to purchase foreign assets; and
(3) Japanese companies are increasingly investing overseas. Clynch (2020) argues
that in the short run, global demand for the JPY can keep the currency’s safe haven
status despite the massive policy easing by the Bank of Japan (BOJ) during the
COVID-19 pandemic. That said, the BOJ’s monetary policy easing may pose a threat
to the JPY’s safe haven status in the long run when the risk appetite is back among
global investors.
Figure 3.3 displays Japan’s REER and the risk-off episodes (the REER value below the
par value means that the JPY is undervalued, while it is overvalued when above the
par). Japan’s REER also tends to increase during the risk-off episodes. That said,
the JPY has been undervalued since October 2012. It implies that from that month
until the end of September 2021 (the last REER observation in our study), the JPY
appreciation during the risk-off episodes might not severely harm Japan’s
competitiveness in international trade.

                          Figure 3: Japan’s REER and Risk-off Episodes




Note: Plotted are Japan’s real effective exchange rate and our calculated risk-off episodes.
Source: BIS, Authors’ calculation.




                                                            7
ADBI Working Paper 1345                                                 Beirne and Sugandi



Bond markets, stock markets, and capital flow dynamics in safe haven destinations
are also subject to sharp fluctuations during periods of heightened financial stress in
global markets.2 For example, the yields of Japanese government bonds (JGBs) tend
to fall during the risk-off episodes due to purchases of JGBs by domestic and foreign
investors. Although the Japanese government debt and the amount of the debt
securities (i.e., JGBs and Japanese government treasury bills—JGTs) has continued to
pile up during the COVID-19 pandemic, global investors still perceive Japanese debt
securities as safe haven assets because most of these securities are owned by
Japanese domestic investors. The yield of the 10-year JGB rose by at most 24 basis
points during the COVID-19 pandemic episode from 24 February to 7 April 2020.

Based on Japan’s Ministry of Finance (MoF) data as of the end of June 2021, foreign
ownership of the Japanese debt securities was recorded at ¥161.8 trillion (about 13%
of the total amount of government debt securities). Foreign investors place their funds
mostly in the JGTs, where the amount of foreign ownership stood at ¥85.4 trillion
(around 51% of the total amount of the JGTs) as of the end of June 2021. While
foreign investors place almost the same amount in the JGBs (¥76.4 trillion as of the
end of June 2021), the share of foreign ownership of foreign investors was only about
7% of the total amount of JGBs (Ministry of Finance Japan 2021). Japanese debt
securities investors have been heavily skewed toward advanced economies that have
large, deep, mature debt securities markets, particularly the United States and the
European Union countries (Shirai and Sugandi 2019). These countries’ government
debt securities have higher yields than those of Japan, thus offering a higher rate
of return to Japanese investors. The low interest rates in Japan have also induced
foreign investors to conduct carry trading, i.e., by borrowing in Japan for investment in
higher-yield countries.
While foreign investors have continued to engage in carry trading during the COVID-19
pandemic, the rising yields of long-term JGBs vis- à-vis the yields of other advanced
economies—largely due to “unlimited scope and length” of the BOJ quantitative—
narrow the premium of Japanese investors’ overseas investments (Clynch 2020;
Pattanaik 2020). This can discourage Japanese investors from investing abroad and
foreign investors from participating in the carry trade.
Unlike the JGBs (and Japanese debt securities), Japanese equities are not regarded
as safe haven assets, however. The benchmark Nikkei-225 stock market index falls
during the risk-off episodes, in line with the movements of major stock indexes in the
United States. Foreign investors have a substantial investment in Japanese equities,
with a share of around 30% in 2020 (CEIC data). Japan’s cross-border equity
investment liabilities towards the United States account for more than half of Japan’s
cross-border equity (International Monetary Fund 2021; Shirai and Sugandi 2019). On
capital flows, foreign investors tend to reduce their investment in Japanese equities
during the risk-off periods. Meanwhile, the net flows of other investments (i.e., cross-
border banking flows) to Japan tend to be, but not always, positive or increasing during
the risk-off periods. Japanese investors tend to repatriate their overseas investment to
domestic banking accounts during the risk-off episodes.
Overall, it is apparent from the basic analysis of the raw data that risk-off episodes tend
to be associated with an appreciating yen exchange rate over the period 1990 to 2021.
The extent of exchange rate appreciation may not be uniform across other major safe
haven destinations, however. In our empirical analysis, we assess the magnitude and



2
    Please refer to Figs A1.1 to A1.7 in Appendix for details.


                                                       8
ADBI Working Paper 1345                                                                 Beirne and Sugandi



duration of impact through which risk-off shocks affect real and financial variables in
Japan, Switzerland, and the US.


4. DATA AND EMPIRICAL METHODOLOGY
We employ a VAR approach to investigate the main financial channels during the risk-
off episodes. While focusing on the Japanese financial markets, we also estimate the
VAR models for Switzerland and the United States for comparison. The generic form of
our VAR models is specified as follows:

            𝑌! = ∑#$%..' 𝑌!"# 𝐴# + 𝑋! 𝐵! + 𝑐! + 𝜀!                                                        (1)

where 𝑌! is the vector of endogenous variables; 𝑋! is the matrix of exogenous
variables; 𝐴# and 𝐵! are the coefficient matrixes; 𝑐! is the vector of constants; and 𝜀! is
the vector of error terms. Indexes 𝑡 and 𝜏 are the time indexes, while 𝑘 is optimum time
lag for the VAR model based on the Akaike Information Criterion (AIC).
The endogenous variables in our VAR model for each country based on their ordering
are: (1) risk-off events (“Risk-off”); (2) log of world uncertainty index (“WUI”); (3) the
spread between the yield of Japan’s or Switzerland’s 10-year government bond and the
10-year US Treasury bond (“Spread”) (only for the Japanese and the Swiss models,
not used for the US models); (4) log of real gross domestic product (“RGDP”); (5) log of
the real effective exchange rate (“REER”); (6) log of the stock market index (“Stock
Index"); (7) net portfolio investment inflows to debt securities as a percentage of
nominal GDP (“Debtsec”); (8) net portfolio investment inflows to equity as a percentage
of nominal GDP (“Equity”); (9) net other portfolio investment inflows as a percentage of
nominal GDP (“Other”); and (10) net inflows of direct investment as a percentage of
nominal GDP (“Direct”). The exogenous variables are the time dummy and the
seasonal dummies.
For each country, our baseline model is a recursively restricted VAR, with impulse
responses generated based on a one-standard deviation structural shock on the
Risk-off variable relative to all endogenous variables in each model. A Cholesky
identification scheme is used. We also estimate the VAR in unrestricted form. In the
unrestricted VAR estimation, each endogenous variable in the model is affected by the
lagged values of itself and other endogenous variables. In the restricted estimation, we
set the model so that the Risk-off variable is only affected by its own lagged values,
while other endogenous variables are affected by each other’s lagged values and are
affected by the lagged values of the Risk-off variable. To make the restrictions, we set
the values of other endogenous variables in the Risk-off equation line of the coefficient
matrix 𝐴# to zeros while keeping the values of the Risk-off variable as it is. Confidence
intervals at the 95% level are provided.
We use working days data that span from 14 January 1999 to 31 March 2021 for
Japan, 13 March 2007 to 31 March 2021 for Switzerland, and 15 January 2002 to
31 March 2021 for the United States.3 The WUI and the REER data are converted from

3
    The use of daily data is used given that the risk-off shocks occurred on a specific day. Interpolating time
    series to higher frequencies is commonly undertaken in order to address issues related to conducting
    empirical work that combines financial and macroeconomic time series. In particular, interpolating from
    lower to higher frequencies is not regarded as being problematic given that the lower frequency
    variables, such as output, are slower moving so that any errors due to the interpolation would only
    marginally affect the impact variables (e.g., Danielsson et al. 2018). Nonetheless, in order to allay
    concerns, we have also carried out the analysis using a weekly and monthly frequencies, the results of
    which are fully consistent with our baseline. These results are shown in Appendix 4.


                                                       9
ADBI Working Paper 1345                                                              Beirne and Sugandi



monthly to working days frequency using the quadratic interpolation method. Data of
the RGDP, Debtsec, Equity, Other, and Direct variables are converted from quarterly
to working day frequency also using the interpolation method. Table 2 lists the
endogenous variables, data, and data sources.

                           Table 2: Variables, Data, and Data Source
Variable                                 Data                                     Data Source
Risk-off           Risk-off event (value: 0, 1)                      Authors’ calculation
Log (WUI)          World Uncertainty Index (WUI) (index unit)        https://worlduncertaintyindex.com/
Spread             • 10-year Japanese government bond yield          Bloomberg
(vis-à-vis US)       (%)
                   • 10-year Switzerland government bond yield
                     (%)
                   • 10-year US Treasury government bond yield
                     (%)
Log (RGDP)         Constant price GDP                                International Monetary Fund (IMF)
Log (REER)         Real effective exchange rate, broad index         Bank for International Settlements
                   (2010 = 100, index unit) of:                      (BIS)
                   • Japan
                   • Switzerland
                   • United States
Log                • Nikkei-225 Index                                Bloomberg
(Stock_Index)      • Swiss Market Index
                   • S&P 500 Index
Debtsec            • Net portfolio investment inflows to debt        • International Monetary Fund (IMF)
                     securities (USD billion)                        • CEIC
                   • GDP at current price (local currency billion)   • Bloomberg
                   • USD/JPY and CHF/USD exchange rate
Equity             • Net portfolio investment inflows to equity      International Monetary Fund (IMF)
                     (USD billion)
                   • GDP at current price (local currency billion)
                   • USD/JPY and CHF/USD exchange rate
Other              • Net other portfolio investment (USD billion)    • International Monetary Fund (IMF)
                   • GDP at current price (local currency billion)   • CEIC
                   • USD/JPY and CHF/USD exchange rate               • Bloomberg
Direct             • Net direct investment (USD billion)             • International Monetary Fund (IMF)
                   • GDP at current price (local currency billion)   • CEIC
                   • USD/JPY and CHF/USD exchange rate               • Bloomberg



5. EMPIRICAL RESULTS
Figures 4 to 8 display the main impulse response function (IRF) results from the
restricted VAR models for Japan, Switzerland, and the US. 4 Real and financial
spillovers to Japan from risk-off shocks are evident via a number of transmission
channels. While risk-off episodes are typically associated with a flight to safe havens,
rising uncertainty in markets is nonetheless broad-based, with safe haven destinations
also subject to heightened uncertainty. Our impulse responses indicate that risk-off
shocks lead to a rise in economic uncertainty, although the response is not always
statistically significant (Figure 4).


4
    The full set of IRFs for both the restricted and unrestricted models are provided in the Appendix. We
    focus the discussion primarily on statistically significant IRFs at conventional levels. Also shown are
    robustness tests based on weekly and monthly frequencies for the primary IRFs.


                                                     10
ADBI Working Paper 1345                                                                                                                         Beirne and Sugandi



            Figure 4: Economic Policy Uncertainty Responses to Risk-off Shocks
                                      in Safe Havens
          Response of LOG(WUI_JP) to RISK Innovation                   Response of LOG(WUI_SZ) to RISK Innovation                   Response of LOG(WUI_US) to RISK Innovation

 .0035                                                                                                                     .005
 .0030                                                        .004
                                                                                                                           .004
 .0025
                                                              .003                                                         .003
 .0020
 .0015                                                        .002                                                         .002
 .0010                                                                                                                     .001
                                                              .001
 .0005                                                                                                                     .000
 .0000                                                        .000
                                                                                                                           -.001
              25         50        75       100         125                25        50        75        100         125                25        50        75        100         125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction; 95% confidence intervals are provided by the dotted lines; the vertical axis represents percentage points
while the horizontal axis refers to the number of days.


For Japan, the response of economic policy uncertainty falls marginally outside
95% confidence intervals, compared to Switzerland and the US where a statistically
significant amplification of domestic economic uncertainty is found. It is notable that the
magnitude and duration of the response of domestic economic policy uncertainty is
very similar across all three safe havens. The lack of statistical significance in the case
of Japan may be linked to the much more muted impact of risk-off episodes on the
volatility of local financial markets given strong expectations of overseas portfolio
holdings repatriated back to Japan priced in by market participants.
On real spillovers of risk-off shocks to safe havens (Figure 5), there is clear evidence
of a negative impact on GDP growth in all safe havens. During risk-off episodes, it may
be intuitive to expect a broad-based decline in global demand from both trade and
financial channels. The findings are most pronounced in the case of Japan as regards
statistical significance. From around 25 days after the risk-off shock, a statistically
significant decline in GDP growth is found, with the negative impact peaking at around
50 days. A broadly similar pattern is found for Switzerland and the US, although the
effect is only marginally statistically significant and short-lived in these cases.

          Figure 5: Output Growth Responses to Risk-off Shocks in Safe Havens
          Response of LOG(RGDP_JP) to RISK Innovation                  Response of LOG(RGDP_SZ) to RISK Innovation                  Response of LOG(RGDP_US) to RISK Innovation


 .0000                                                        .0002                                                        .0000
 -.0002                                                                                                                    -.0002
                                                              .0000
 -.0004
                                                              -.0002                                                       -.0004
 -.0006
                                                              -.0004                                                       -.0006
 -.0008

 -.0010                                                       -.0006                                                       -.0008
               25        50        75       100         125                  25       50        75       100         125                 25        50        75       100         125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction; 95% confidence intervals are provided by the dotted lines; the vertical axis represents percentage points
while the horizontal axis refers to the number of days.




                                                                                          11
ADBI Working Paper 1345                                                                                                                       Beirne and Sugandi



Financial flows to safe havens due to risk-off episodes can be expected to lead to real
exchange rate appreciations, the competitiveness impacts of which can be important
contributors to negative real effects over time. The precise effect also depends on the
speed of possible policy reaction to counteract appreciating exchange rate, notable
intervention by the central bank in foreign exchange markets. Our impulse response
analysis shows differences in the responses of REERs for Japan, Switzerland, and the
US to risk-off shocks (Figure 6).

                    Figure 6: REER Responses to Risk-off Shocks in Safe Havens

         Response of LOG(REER_JP) to RISK Innovation                  Response of LOG(REER_SZ) to RISK Innovation                  Response of LOG(REER_US) to RISK Innovation

                                                             .0000                                                        .0010
 .0016
                                                                                                                          .0008
 .0012                                                       -.0004                                                       .0006
                                                                                                                          .0004
 .0008                                                       -.0008
                                                                                                                          .0002
 .0004                                                       -.0012                                                       .0000
                                                                                                                          -.0002
 .0000                                                       -.0016
                                                                                                                          -.0004
              25        50        75       100         125                 25        50        75       100         125                 25        50        75       100         125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction. 95% confidence intervals are provided by the dotted lines. The vertical axis represents percentage points
while the horizontal axis refers to the number of days.


For the Japanese yen, a risk-off shock results in the expected exchange rate
appreciation. This appreciating effect of the yen peaks at around 40 days and is
persistently statistically significant over the time horizon duration. For the US, we
observe a significant real appreciation immediately after the risk-off shock, although the
effect loses statistical significance after a few days.
By contrast, we find the opposite effect for Switzerland, with the Swiss franc
depreciating significantly, which may seem to be counterintuitive. It is important to bear
in mind, however, that the Swiss central bank actively and aggressively intervenes
in foreign exchange markets to ensure the competitiveness in its export-dependent
economy. The Bank of Japan, by contrast, tends not to intervene strongly in foreign
exchange markets. This is underpinned by its preference to allow interest rate yield
differentials vis-à-vis the US bear the adjustment, which would keep the USD–JPY
bilateral exchange rate in a narrow range. In the case of Japan, the response of GDP
growth given an appreciating REER suggests that exchange rate and trade channels
are important contributing factors to negative real spillovers. In other words, safe haven
financial flows to Japan in periods of heightened global risk aversion dampen economic
growth via appreciating exchange rate effects.
On long-term yield differentials relative to the US (Figure 7), also reflecting rising
country-specific risk, a significant and positive response of long yield spreads for the
Japanese government bond market is found. The effect peaks at around 40 days after
the risk-off shock but remains persistent and statistically significant over the estimation
duration. A similar effect is found in the case of Swiss bond spreads.




                                                                                      12
ADBI Working Paper 1345                                                                                                                              Beirne and Sugandi



 Figure 7: Sovereign Bond Spread Responses to Risk-off Shocks in Safe Havens

                                          Response of SPREAD_JP to RISK Innovation                         Response of SPREAD_SZ to RISK Innovation

                              .016
                              .014                                                             .016
                              .012
                                                                                               .012
                              .010
                              .008                                                             .008
                              .006
                                                                                               .004
                              .004
                              .002                                                             .000

                                             25        50         75          100       125                   25        50         75         100        125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction; 95% confidence intervals are provided by the dotted lines; the vertical axis represents percentage points
while the horizontal axis refers to the number of days.


On sovereign bond spreads, widening spreads underscore the dominance of the US
dollar as the main global safe haven currency. During risk-off episodes, flows to US
Treasuries imply that even other safe haven destinations for financial flows will face
some amplification is sovereign borrowing costs. This also relates to the theoretical
literature pointing towards a significant role of liquidity in affecting asset pricing (e.g.,
Vayanos 2004; Caballero and Krishnamurthy 2008; Brunnermeier and Pederson 2009)
For the stock market in safe havens. (Figure 8), the risk-off shock leads to an
immediate positive effect in Japan, in line with a surge to safety. The significance of the
shock becomes negative thereafter, however. A similar response is found in the US
stock market, while no significant effect is found for Switzerland. Time varying impacts
of market volatility on equity risk premia and risk aversion across safe havens are
important considerations in this regard (e.g., Bekaert, Engstrom, and Xing 2009).

              Figure 8: Equity Market Responses to Risk-off Shocks in Safe Havens

        Response of LOG(STOCK_IDX_JP) to RISK Innovation                Response of LOG(STOCK_IDX_SZ) to RISK Innovation               Response of LOG(STOCK_IDX_US) to RISK Innovation

                                                               .0020                                                          .0010
 .002
                                                               .0015                                                          .0005
 .001                                                          .0010                                                          .0000
                                                               .0005                                                          -.0005
 .000
                                                               .0000                                                          -.0010
-.001                                                          -.0005                                                         -.0015
                                                               -.0010                                                         -.0020
-.002
                                                               -.0015                                                         -.0025
               25        50          75        100       125                    25       50           75       100      125                   25        50        75        100       125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction; 95% confidence intervals are provided by the dotted lines; the vertical axis represents percentage points
while the horizontal axis refers to the number of days.


Turning to capital flows, Figures 9 and 10 show the responses in portfolio debt and
portfolio equity flows to safe havens. Overall, and contrary to expectations, we do not
find a significant effect in the response of portfolio flows to Japan to a risk-off shock.
That said, this finding is in line with Botman, De Carvalho Filho, and Lam (2013), who
suggest that Japan may be subject to portfolio rebalancing triggered by risk-off




                                                                                           13
ADBI Working Paper 1345                                                                                                                      Beirne and Sugandi



episodes via offshore trading in derivatives markets that are not captured in official
balance of payments transactions.

         Figure 9: Portfolio Debt Flow Responses to Risk-off Shocks in Safe Havens
          Response of DEBTSEC_JP to RISK Innovation                  Response of DEBTSEC_SZ to RISK Innovation                   Response of DEBTSEC_US to RISK Innovation

 .015
                                                             .00                                                        .020
 .010
                                                             -.01                                                       .016
 .005
                                                             -.02                                                       .012
 .000
                                                             -.03                                                       .008
 -.005
                                                             -.04                                                       .004
 -.010
                                                             -.05                                                       .000
 -.015
              25        50        75       100        125                25        50         75      100        125                 25        50        75        100        125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction; 95% confidence intervals are provided by the dotted lines; the vertical axis represents percentage points
while the horizontal axis refers to the number of days.


While no significant effect is found for portfolio debt responses to risk-off in the case of
Japan (similar to Switzerland), the response in the US is positive and statistically
significant. This is in line with conventional expectations that in times of heightened
financial stress, US debt securities are the preferred destination for financial flows
by investors. As described by Caballero and Krishnamurthy (2009), these flows of
primarily nonspeculative capital can lead to excessive leverage by financial institutions
as risk-free assets are sold to foreigners during these periods. On portfolio equity
responses (Figure 10), we find some evidence of a statistically significance positive
response for equity flows to Switzerland, but no significance for Japan or the US.

   Figure 10: Portfolio Equity Flow Responses to Risk-off Shocks in Safe Havens
          Response of EQUITY_JP to RISK Innovation                    Response of EQUITY_SZ to RISK Innovation                     Response of EQUITY_US to RISK Innovation

                                                               .06
 .005
                                                               .05                                                       .012
 .000                                                          .04                                                       .008
-.005                                                          .03
                                                                                                                         .004
                                                               .02
-.010
                                                               .01                                                       .000
-.015
                                                               .00                                                       -.004
              25        50         75        100       125                25        50         75       100       125                 25        50        75        100        125

Note: Reported are the IRFs based on equation (1), using a Cholesky identification scheme and block recursive
restriction; 95% confidence intervals are provided by the dotted lines; the vertical axis represents percentage points
while the horizontal axis refers to the number of days.


Comparing real and financial spillovers from risk-off shocks in Japan to the case of the
US and Switzerland suggests an idiosyncrasy to the dynamics at play in Japan. On real
spillovers, the effect of risk-off shocks has only a marginal and short-lived significant
effect on GDP growth in the US or Switzerland, while a statistically significant negative
effect of greater magnitude is found for Japan after around 25 days, remaining
persistent thereafter. Japan’s protracted lower relative GDP growth may make it more


                                                                                         14
ADBI Working Paper 1345                                                 Beirne and Sugandi



susceptible to shocks. On financial spillovers, the exchange rate effect is specific to
Japan, weighing on competitiveness and growth.


6. CONCLUSIONS
This paper examines real and financial spillovers of risk-off episodes in safe haven
destinations over the period 1990 to 2021. We show that dynamics for Japan appear to
be different to those of Switzerland and the US in four main ways. First, over the
estimation period, in response to risk-off episodes, the yen REER appreciates sharply
and significantly, with the effect persisting over time. Second, no significant effect on
portfolio flows to Japan are found, in spite of the appreciating exchange rate effect,
suggesting a rapid adjustment of financial markets to shifts in equilibrium exchange
rates. Third, negative real spillovers from risk-off shocks appear to only apply to Japan.
Fourth, risk-off shocks do not have a statistically significant effect on domestic
economic policy uncertainty in Japan, which may be related to the strong expectations
priced in of overseas portfolio holdings repatriated back to Japan.
While our findings relate to the period 1990 to 2021, when Japan was largely running
current account surpluses, in the more recent period during 2022, the combination of
widening interest rate differentials between the US and Japan and the effects of rising
commodity prices due to the Ukraine crisis and Japan’s status as a net energy
importer, has led to a sharp depreciation of the yen. The worsening of the balance of
payments position driven by trade deficits in Japan have contributed to yen fluctuations
out of line with traditional expectations for safe haven currencies during periods of
global risk aversion. This is related to the nature of the 2022 crisis, which is unusual in
the sense that US monetary policy is tightening aggressively, commodity prices are
rising and pushing Japan’s current account balance towards deficit.
Nonetheless, our findings have important implications for policymakers. Effective
exchange rate management would appear to be particularly important in the case of
Japan, also related to its transmission to the real economy. Policy makers should
be vigilant to potential volatility in currency markets and ensure that appropriate
countercyclical adjustment mechanisms are available from the suite of fiscal, monetary,
and macroprudential policy tools. In addition, persistence identified in bond spreads
and portfolio debt securities may contribute to a buildup of financial vulnerabilities
and risks to financial stability over the longer term, underscoring the need for careful
monitoring by policymakers, in particular by central banks and financial supervisors.




                                            15
ADBI Working Paper 1345                                                Beirne and Sugandi




REFERENCES
Balcilara, M., Demirer, R., Gupta, R., and Wohar, M.E. 2020. The Effect of Global and
        Regional Stock Market Shocks on Safe Haven Assets. Structural Change and
        Economic Dynamics 54: 297–308.
Baur, D., and Lucey, B. 2010. Is Gold a Hedge or a Safe Haven? An Analysis of Stocks,
       Bonds and Gold. The Financial Review 45(2): 217–229.
Beckmann, J., and Czudaj, R. 2016. Exchange Rate Expectations and Economic
     Policy Uncertainty. European Journal of Political Economy 47: 148–162.
———. 2017. Exchange Rate Expectations Since the Financial Crisis: Performance
    Evaluation and the Role of Monetary Policy and Safe Haven. Journal of
    International Money and Finance 74: 283–300.
Bekaert, G., Engstrom, E., and Xing, Y. 2009. Risk, Uncertainty, and Asset Prices.
      Journal of Financial Economics 91(1): 59–82.
Belke, A., and Volz, U. 2020. The Yen Exchange Rate and the Hollowing Out of the
       Japanese Industry. Open Economies Review 31: 371–406.
Botman, D., De Carvalho Filho, I., and Lam, W.R. 2013. The Curious Case of the Yen
      as a Safe Haven Currency: A Forensic Analysis. IMF Working Paper WP/13/228.
      Washington, DC: International Monetary Fund.
Brunnermeier, M. K., and Pederson, L.H. 2009. Market Liquidity and Funding Liquidity.
      Review of Financial Studies 22: 2201–2238.
Bussière, M., Lopez, C., and Tille, C. 2013. Currency Crises in Reverse: Do Large Real
       Exchange Rate Appreciations Matter for Growth? MPRA Paper No. 44096.
Caballero, R. J., and Krishnamurthy, A. 2008. Collective Risk Management in a Flight
       to Quality Episode. Journal of Finance 63: 2195–2230.
Caballero, R. J., and Krishnamurthy, A. 2009. Global Imbalances and Financial
       Fragility. American Economic Review 99(2): 584–588.
Cho, D., and Han, H. 2021. The Tail Behavior of Safe Haven Currencies: A Cross-
      quantilogram Analysis. Journal of International Financial Markets, Institutions
      & Money 70: 101257.
Clynch, H. 2020. The Puzzle of the Japanese Yen’s Safe-Haven Status.
       https://disruptionbanking.com/2021/02/10/the-puzzle-of-the-japanese-yens-
       safe-haven-status/
Danielsson, J., Valenzuela, M., and Zer, I. 2018. “Learning from History: Volatility and
       Financial Crises”. The Review of Financial Studies 31(7): 2774–2805.
De Bock, R., and De Carvalho Filho, I. 2013.The Behavior of Currencies during Risk-off
      Episodes. IMF Working Paper 13/08.
Dekle, R. 1998. The Yen and Japanese Manufacturing Employment. Journal of
       International Money and Finance 17:785–801
Fatum, R., and Yamamoto, Y. 2015. Intra-safe Haven Currency Behavior During the
      Global Financial Crisis. Journal of International Money and Finance 66: 49–64.
Grisse, C., and Nitschka, T. 2015. On financial risk and the safe haven characteristics
       of Swiss franc exchange rates. Journal of Empirical Finance 32: 153–164.




                                           16
ADBI Working Paper 1345                                               Beirne and Sugandi



Habib, M. H., and Stracca, L. 2012. Getting Beyond Carry Trade: What Makes a Safe
       Haven Currency? Journal of International Economics 87(1): 50–64.
Habib, M. H., Stracca, L., and Venditti, F. 2020. The Fundamentals of Safe Assets.
       Journal of International Money and Finance 102: 102119.
Horioka, C. Y., Nomoto, T., and Terada-Hagiwara, A. 2014. Why Has Japan’s Massive
       Government Debt Not Wreaked Havoc (Yet)? The Japanese Political Economy
       40(2): 3–23.
Hossfeld, O., and MacDonald, R. 2014. Carry Funding and Safe Haven Currencies:
      A Threshold Regression Approach. Journal of International Money and Finance
      59: 185–202.
Imakubo, K., Kamada, K., and Kan, K. 2015. A New Technique for Estimating Currency
      Premiums. Bank of Japan Working Paper Series No 15-E-9.
International Monetary Fund. 2021. Coordinated Portfolio Investment Survey (CPIS).
       https://data.imf.org/?sk=B981B4E3-4E58-467E-9B90-9DE0C3367363.
Iwaisako, T. and Nakata, H. 2017. Impact of Exchange Rate Shocks on Japanese
       Exports: Quantitative Assessment Using a Structural VAR Model. Journal of the
       Japanese and International Economies 46:1–16.
Jäggi, A., Schlegel, M., and Zanetti, A.2019. Macroeconomic Surprises, Market
       Environment, and Safe-haven Currencies. Swiss Journal of Economics and
       Statistics 155:5.
Lam, W.R., and Tokuoka, K. 2013. Assessing the Risks to the Japanese Government
      Bond (JGB) Market. Journal of International Commerce, Economic and Policy
      4(1):1-15.
Lewis, Leo. 2020. Why the Japanese Yen Is Not the Haven Asset it Once Was.
       https://www.ft.com/content/23d721cc-3609-11ea-a6d3-9a26f8c3cba4
Masujima, Y. 2017. Safe Haven Currency and Market Uncertainty: Yen, Renminbi,
      Dollar, and Alternatives. RIETI Discussion Paper Series 17-E-048. Tokyo:
      Research Institute of Economy, Trade and Industry.
Min, H-G, McDonald, J.A., and Shin, S-A. 2016. What Makes a Safe Haven? Equity
       and Currency Returns for Six OECD Countries during the Financial Crisis.
       Annals of Economics and Finance 17-2: 365–402.
Ministry of Finance of Japan. (2021). Japanese Government Bond: Monthly Newsletter
        of the Ministry of Finance, November 2021.
Nishigaki, H. 2007. Relationship Between the Yen Carry Trade and the Related
       Financial Variables. Economics Bulletin 13(2): 1-7.
Pattanaik, Swaha. 2020. Breakingviews – Japanese Bond Market Shift Spells Stronger
       Yen. https://www.reuters.com/article/us-japan-bonds-boj-breakingviews-
       idUSKBN2480FR.
Ranaldo, A., and Söderlind, P. 2010. Safe Haven Currencies. Review of Finance
      14: 385–407.
Rogoff, K. S., and Tashiro, T. 2015. Japan’s Exorbitant Privilege. Journal of the
       Japanese and International Economies 35: 43–61.




                                           17
ADBI Working Paper 1345                                                Beirne and Sugandi



Shirai, S., and E.A. Sugandi 2019. Growing Global Demand for Cash. International
        Business Research 12(12): 74–92.
Todorova, V. 2020. Safe Haven Currencies. Economic Alternatives 4: 579–591.
Vayanos, D. 2004. Flight to Quality, Flight to Liquidity, and the Pricing of Risk. NBER
      Working Paper No. 10327.




                                           18
ADBI Working Paper 1345                                              Beirne and Sugandi




APPENDIX 1: FINANCIAL MARKETS AND RISK-OFF
EVENTS IN JAPAN
          Figure A1.1: The 10-Year JGB Yields (%) and the Risk-off Episodes




Source: Bloomberg, Authors’ calculation.


                     Figure A1.2: Nikkei-225 Index and Risk-off Episodes




Source: Bloomberg, Authors’ calculation.




                                             19
ADBI Working Paper 1345                                           Beirne and Sugandi



            Figure A1.3: Net Debt Securities Investment to Japan (% of GDP)
                                 and Risk-off Episodes




Source: Bloomberg, Authors’ calculation.


  Figure A1.4: Net Equity Investment to Japan (% of GDP) and Risk-off Episodes




Source: Bloomberg, Authors’ calculation.




                                           20
ADBI Working Paper 1345                                        Beirne and Sugandi



  Figure A1.5: Net Other Investment to Japan (% of GDP) and Risk-off Episodes




Source: Bloomberg, Authors’ calculation.


  Figure A1.6: Net Direct Investment to Japan (% of GDP) and Risk-off Episodes




Source: Bloomberg, Authors’ calculation.




                                           21
ADBI Working Paper 1345                                    Beirne and Sugandi



  Figure A1.7: Yield Spread Between the 10Y US and Japan Government Bonds




Source: Bloomberg, Authors’ calculation.




                                           22
ADBI Working Paper 1345                                                                                    Beirne and Sugandi




APPENDIX 2: RESPONSES TO RISK-OFF SHOCKS:
RESTRICTED VAR MODELS
                      Figure A2.1: Real and Financial Spillovers in Japan
               Response of RISK to RISK Innovation                           Response of LOG(WUI_JP) to RISK Innovation

     .10                                                         .0035
                                                                 .0030
     .08
                                                                 .0025
     .06                                                         .0020
                                                                 .0015
     .04
                                                                 .0010
     .02                                                         .0005
                                                                 .0000
     .00
                25         50        75        100         125                    25        50        75       100         125

             Response of SPREAD_JP to RISK Innovation                        Response of LOG(RGDP_JP) to RISK Innovation

     .016
                                                                 .0000
     .014
     .012                                                        -.0002
     .010
                                                                 -.0004
     .008
     .006                                                        -.0006
     .004                                                        -.0008
     .002
                                                                 -.0010
                 25        50        75        100         125                    25        50        75       100         125

             Response of LOG(REER_JP) to RISK Innovation                  Response of LOG(STOCK_IDX_JP) to RISK Innovation

     .0016                                                       .002

     .0012                                                       .001

     .0008                                                       .000

     .0004                                                       -.001

     .0000                                                       -.002

                  25        50        75       100         125                   25        50        75        100         125

             Response of DEBTSEC_JP to RISK Innovation                        Response of EQUITY_JP to RISK Innovation

      .015
                                                                 .005
      .010
      .005                                                       .000

      .000                                                       -.005
     -.005                                                       -.010
     -.010
                                                                 -.015
     -.015
                 25         50        75       100         125                   25        50        75        100         125

             Response of OTHER_JP to RISK Innovation                          Response of DIRECT_JP to RISK Innovation
      .03                                                         .004
                                                                  .003
      .02                                                         .002
                                                                  .001
      .01                                                         .000
                                                                 -.001
      .00                                                        -.002
                                                                 -.003
     -.01                                                        -.004
                 25        50        75        100         125                   25        50        75        100         125




                                                             23
ADBI Working Paper 1345                                                                                    Beirne and Sugandi



                Figure A2.2: Real and Financial Spillovers in Switzerland
                 Response of RISK to RISK Innovation                        Response of LOG(WUI_SZ) to RISK Innovation
     .12
     .10                                                          .004
     .08                                                          .003
     .06
                                                                  .002
     .04
                                                                  .001
     .02
                                                                  .000
     .00
                 25         50        75        100         125                  25        50         75       100         125

              Response of SPREAD_SZ to RISK Innovation                       Response of LOG(RGDP_SZ) to RISK Innovation


     .016                                                         .0002

     .012                                                         .0000

     .008                                                         -.0002

     .004                                                         -.0004
     .000
                                                                  -.0006
                  25        50        75        100         125                    25       50        75        100        125

              Response of LOG(REER_SZ) to RISK Innovation                  Response of LOG(STOCK_IDX_SZ) to RISK Innovation

      .0000                                                       .0020
                                                                  .0015
     -.0004
                                                                  .0010
     -.0008                                                       .0005
                                                                  .0000
     -.0012                                                       -.0005
                                                                  -.0010
     -.0016
                                                                  -.0015
                   25        50        75       100         125                    25       50        75        100        125

              Response of DEBTSEC_SZ to RISK Innovation                      Response of EQUITY_SZ to RISK Innovation

                                                                  .06
      .00
                                                                  .05
     -.01
                                                                  .04
     -.02
                                                                  .03
     -.03                                                         .02
     -.04                                                         .01
     -.05                                                         .00
                  25        50        75        100         125                 25         50        75        100         125

              Response of OTHER_SZ to RISK Innovation                        Response of DIRECT_SZ to RISK Innovation
      .20                                                         .00
      .16                                                         -.02
      .12                                                         -.04
      .08                                                         -.06

      .04                                                         -.08

      .00                                                         -.10
                                                                  -.12
     -.04
                  25        50        75        100         125                  25        50        75        100         125




                                                              24
ADBI Working Paper 1345                                                                                          Beirne and Sugandi



                Figure A2.3: Real and Financial Spillovers in United States
                   Response of RISK to RISK Innovation                             Response of LOG(WUI_US) to RISK Innovation

     .10                                                              .005

     .08                                                              .004
                                                                      .003
     .06
                                                                      .002
     .04
                                                                      .001
     .02                                                              .000
     .00                                                              -.001
                   25         50         75          100       125                     25        50        75        100         125

               Response of LOG(RGDP_US) to RISK Innovation                         Response of LOG(REER_US) to RISK Innovation
                                                                      .0010
      .0000                                                           .0008
                                                                      .0006
     -.0002
                                                                      .0004
     -.0004                                                           .0002

     -.0006                                                           .0000
                                                                      -.0002
     -.0008                                                           -.0004
                     25        50            75       100       125                     25        50        75       100         125

              Response of LOG(STOCK_IDX_US) to RISK Innovation                     Response of DEBTSEC_US to RISK Innovation

      .0010
                                                                      .020
      .0005
      .0000                                                           .016

     -.0005                                                           .012
     -.0010                                                           .008
     -.0015
                                                                      .004
     -.0020
                                                                      .000
     -.0025
                     25        50            75       100       125                    25        50        75        100         125

                 Response of EQUITY_US to RISK Innovation                           Response of OTHER_US to RISK Innovation

                                                                      .000
      .012
                                                                      -.005
      .008
                                                                      -.010
      .004
                                                                      -.015
      .000
                                                                      -.020
     -.004
                                                                      -.025
                    25         50            75      100       125                     25        50        75        100         125

                                                  Response of DIRECT_US to RISK Innovation

                                     .002
                                     .000
                                     -.002
                                     -.004
                                     -.006
                                     -.008
                                                     25        50             75       100        125




                                                                    25
ADBI Working Paper 1345                                                                                    Beirne and Sugandi




APPENDIX 3: RESPONSES TO RISK-OFF SHOCKS:
UNRESTRICTED VAR MODELS
                      Figure A3.1: Real and Financial Spillovers in Japan
               Response of RISK to RISK Innovation                           Response of LOG(WUI_JP) to RISK Innovation
     .10
                                                                 .0028
     .08                                                         .0024
                                                                 .0020
     .06                                                         .0016
     .04                                                         .0012
                                                                 .0008
     .02                                                         .0004
                                                                 .0000
     .00
                25         50        75        100         125                    25        50        75       100         125

             Response of SPREAD_JP to RISK Innovation                        Response of LOG(RGDP_JP) to RISK Innovation
     .014
     .012                                                        .0000
     .010                                                        -.0002
     .008
                                                                 -.0004
     .006
     .004                                                        -.0006
     .002
                                                                 -.0008
                 25        50        75        100         125                    25        50        75       100         125

             Response of LOG(REER_JP) to RISK Innovation                  Response of LOG(STOCK_IDX_JP) to RISK Innovation

     .0014                                                       .002
     .0012
     .0010                                                       .001
     .0008
                                                                 .000
     .0006
     .0004
                                                                 -.001
     .0002
     .0000
                                                                 -.002
                  25        50        75       100         125                   25        50        75        100         125

             Response of DEBTSEC_JP to RISK Innovation                        Response of EQUITY_JP to RISK Innovation
                                                                 .008
      .010                                                       .004
      .005                                                       .000
      .000                                                       -.004

     -.005                                                       -.008

     -.010                                                       -.012
                                                                 -.016
                 25         50        75       100         125                   25        50        75        100         125

              Response of OTHER_JP to RISK Innovation                         Response of DIRECT_JP to RISK Innovation
      .025
                                                                 .003
      .020                                                       .002
      .015                                                       .001
      .010                                                       .000
      .005                                                       -.001
      .000                                                       -.002
     -.005                                                       -.003
     -.010                                                       -.004
                 25         50        75       100         125                   25        50        75        100         125




                                                             26
ADBI Working Paper 1345                                                                                    Beirne and Sugandi



                Figure A3.2: Real and Financial Spillovers in Switzerland
                 Response of RISK to RISK Innovation                        Response of LOG(WUI_SZ) to RISK Innovation

                                                                  .004
     .10

     .08                                                          .003

     .06                                                          .002
     .04
                                                                  .001
     .02

     .00                                                          .000
                 25         50        75        100         125                  25        50         75       100         125

              Response of SPREAD_SZ to RISK Innovation                       Response of LOG(RGDP_SZ) to RISK Innovation

     .016
                                                                   .0002
     .012                                                          .0001
                                                                   .0000
     .008                                                         -.0001
                                                                  -.0002
     .004                                                         -.0003
                                                                  -.0004
     .000                                                         -.0005
                  25        50        75        100         125                    25       50        75        100        125

              Response of LOG(REER_SZ) to RISK Innovation                  Response of LOG(STOCK_IDX_SZ) to RISK Innovation

      .0000
                                                                  .0015
     -.0002
     -.0004                                                       .0010
     -.0006                                                       .0005
     -.0008                                                       .0000
     -.0010                                                       -.0005
     -.0012
                                                                  -.0010
     -.0014
                   25        50        75       100         125                    25       50        75        100        125

              Response of DEBTSEC_SZ to RISK Innovation                      Response of EQUITY_SZ to RISK Innovation

                                                                  .05
      .00
                                                                  .04
     -.01
                                                                  .03
     -.02
                                                                  .02
     -.03
                                                                  .01
     -.04
                                                                  .00
     -.05
                  25        50        75        100         125                 25         50        75        100         125

              Response of OTHER_SZ to RISK Innovation                        Response of DIRECT_SZ to RISK Innovation

                                                                  .00
     .15
                                                                  -.02
     .10                                                          -.04

     .05                                                          -.06

                                                                  -.08
     .00
                                                                  -.10

                 25         50        75        100         125                  25        50        75        100         125




                                                              27
ADBI Working Paper 1345                                                                                          Beirne and Sugandi



              Figure A3.3: Real and Financial Spillovers in the United States
                   Response of RISK to RISK Innovation                             Response of LOG(WUI_US) to RISK Innovation

     .10
                                                                      .004
     .08
                                                                      .003
     .06
                                                                      .002
     .04
                                                                      .001
     .02
                                                                      .000
     .00
                   25         50         75          100       125                     25        50        75        100         125

                Response of LOG(RGDP_US) to RISK Innovation                        Response of LOG(REER_US) to RISK Innovation
      .0001
      .0000                                                           .0006
     -.0001
                                                                      .0004
     -.0002
     -.0003                                                           .0002
     -.0004
                                                                      .0000
     -.0005
     -.0006                                                           -.0002

                     25        50            75       100       125                     25        50        75       100         125

              Response of LOG(STOCK_IDX_US) to RISK Innovation                     Response of DEBTSEC_US to RISK Innovation


      .0005                                                           .016

      .0000                                                           .012
     -.0005
                                                                      .008
     -.0010
                                                                      .004
     -.0015
                                                                      .000
     -.0020
                     25        50            75       100       125                    25        50        75        100         125

                 Response of EQUITY_US to RISK Innovation                           Response of OTHER_US to RISK Innovation

      .012                                                            .000
      .010
      .008                                                            -.004
      .006                                                            -.008
      .004
      .002                                                            -.012
      .000
                                                                      -.016
     -.002
     -.004                                                            -.020
                    25         50            75      100       125                      25        50        75       100         125

                                                  Response of DIRECT_US to RISK Innovation

                                     .002

                                     .000

                                     -.002

                                     -.004

                                     -.006

                                                     25        50             75        100       125




                                                                    28
ADBI Working Paper 1345                                                                                                                                               Beirne and Sugandi




APPENDIX 4: DAILY, WEEKLY, AND MONTHLY IMPULSE
RESPONSE FUNCTIONS (IRFS) OF THE RESTRICTED
VAR MODELS
        Figure A4.1: Economic Policy Uncertainty Responses to Risk-off Shocks
                                   in Safe Havens
        •        Daily
            Response of LOG(WUI_JP) to RISK Innovation                         Response of LOG(WUI_SZ) to RISK Innovation                               Response of LOG(WUI_US) to RISK Innovation

.0035                                                                                                                                           .005
.0030                                                                  .004
                                                                                                                                                .004
.0025
                                                                       .003                                                                     .003
.0020
.0015                                                                  .002                                                                     .002
.0010                                                                                                                                           .001
                                                                       .001
.0005                                                                                                                                           .000
.0000                                                                  .000
                                                                                                                                                -.001
                25            50        75            100        125                     25             50         75          100        125                 25            50        75           100        125




        •        Weekly
              Response of LOG(WUI_JP) to RISK Innovation                                Response of LOG(WUI_SZ) to RISK Innovation                          Response of LOG(WUI_US) to RISK Innovation
                                                                       .010
                                                                                                                                                .012
.006
                                                                       .008                                                                     .010
.005
                                                                       .006                                                                     .008
.004
                                                                       .004                                                                     .006
.003

.002                                                                   .002                                                                     .004

.001                                                                   .000                                                                     .002

.000                                                                                                                                            .000
                                                                       -.002
        5        10      15        20    25     30          35    40               5          10   15         20    25    30         35    40           5      10      15        20    25     30         35    40




        •        Monthly
              Response of LOG(WUI_JP) to RISK Innovation                               Response of LOG(WUI_SZ) to RISK Innovation                           Response of LOG(WUI_US) to RISK Innovation

                                                                                                                                                .02
.010
                                                                       .03
.005                                                                                                                                            .01
                                                                       .02
.000
                                                                                                                                                .00
-.005                                                                  .01

-.010                                                                                                                                           -.01
                                                                       .00
-.015
                                                                                                                                                -.02
        5         10     15        20    25      30         35    40           5          10       15        20    25     30         35    40           5      10      15        20   25      30         35    40




                                                                                                             29
ADBI Working Paper 1345                                                                                                                                                Beirne and Sugandi



         Figure A4.2: Output Growth Responses to Risk-off Shocks in Safe Havens
         •          Daily
         Response of LOG(RGDP_JP) to RISK Innovation                               Response of LOG(RGDP_SZ) to RISK Innovation                            Response of LOG(RGDP_US) to RISK Innovation


.0000                                                                     .0002                                                                  .0000
-.0002                                                                                                                                           -.0002
                                                                          .0000
-.0004
                                                                          -.0002                                                                 -.0004
-.0006
                                                                          -.0004                                                                 -.0006
-.0008

-.0010                                                                    -.0006                                                                 -.0008
                    25            50        75           100        125                   25            50        75            100        125                   25            50        75           100        125




         •          Weekly
                 Response of LOG(RGDP_JP) to RISK Innovation                            Response of LOG(RGDP_SZ) to RISK Innovation                           Response of LOG(RGDP_US) to RISK Innovation

                                                                          .0008
.0000
                                                                                                                                                 .0000
-.0004                                                                    .0004

-.0008                                                                    .0000                                                                  -.0004

-.0012
                                                                          -.0004                                                                 -.0008
-.0016
                                                                          -.0008
                                                                                                                                                 -.0012
-.0020

             5       10      15        20    25     30         35    40            5       10      15        20    25      30         35    40            5       10      15        20    25     30         35    40




         •          Monthly
                 Response of LOG(RGDP_JP) to RISK Innovation                           Response of LOG(RGDP_SZ) to RISK Innovation                            Response of LOG(RGDP_US) to RISK Innovation

.003                                                                      .004
                                                                                                                                                 .000
.002                                                                      .003

.001                                                                      .002                                                                   -.001

.000                                                                      .001                                                                   -.002
-.001                                                                     .000
                                                                                                                                                 -.003
-.002                                                                     -.001
                                                                          -.002                                                                  -.004
-.003
-.004                                                                     -.003                                                                  -.005
         5           10     15         20   25      30         35    40            5       10      15        20    25      30         35    40            5       10     15         20   25      30         35    40




                                                                                                         30
ADBI Working Paper 1345                                                                                                                                                 Beirne and Sugandi



                         Figure A4.3: REER Responses to Risk-off Shocks in Safe Havens
         •          Daily
         Response of LOG(REER_JP) to RISK Innovation                                Response of LOG(REER_SZ) to RISK Innovation                            Response of LOG(REER_US) to RISK Innovation

                                                                           .0000                                                                   .0010
.0016
                                                                                                                                                   .0008
.0012                                                                      -.0004                                                                  .0006
                                                                                                                                                   .0004
.0008                                                                      -.0008
                                                                                                                                                   .0002
.0004                                                                      -.0012                                                                  .0000
                                                                                                                                                  -.0002
.0000                                                                      -.0016
                                                                                                                                                  -.0004
                   25             50        75         100           125                  25             50        75            100        125                   25            50        75           100        125




         •          Weekly
                  Response of LOG(REER_JP) to RISK Innovation                            Response of LOG(REER_SZ) to RISK Innovation                           Response of LOG(REER_US) to RISK Innovation

                                                                                                                                                  .0020
.0028
                                                                           .0000
.0024
                                                                                                                                                  .0015
.0020                                                                      -.0005
.0016                                                                      -.0010                                                                 .0010
.0012
.0008                                                                      -.0015                                                                 .0005
.0004                                                                      -.0020
                                                                                                                                                  .0000
.0000
                                                                           -.0025
-.0004
                                                                                                                                                  -.0005
             5          10   15        20    25      30         35    40            5       10      15        20    25      30         35    40            5       10      15        20   25      30         35    40




         •          Monthly
                 Response of LOG(REER_JP) to RISK Innovation                            Response of LOG(REER_SZ) to RISK Innovation                            Response of LOG(REER_US) to RISK Innovation

.010                                                                       .002
                                                                                                                                                  .006
.008
                                                                           .000                                                                   .004
.006

.004                                                                                                                                              .002
                                                                           -.002
.002
                                                                                                                                                  .000
                                                                           -.004
.000
                                                                                                                                                  -.002
-.002
                                                                           -.006
-.004                                                                                                                                             -.004
         5          10       15        20    25      30         35    40            5       10     15         20    25      30         35    40            5      10      15         20   25      30         35    40




                                                                                                          31
ADBI Working Paper 1345                                                                                                     Beirne and Sugandi



              Figure A4.4: Sovereign Bond Spread Responses to Risk-off Shocks
                                       in Safe Havens
   •          Daily
                    Response of SPREAD_JP to RISK Innovation                               Response of SPREAD_SZ to RISK Innovation

    .016
    .014                                                                        .016
    .012
                                                                                .012
    .010
    .008                                                                        .008
    .006
                                                                                .004
    .004
    .002                                                                        .000

                         25             50        75           100        125                 25            50        75            100        125




   •          Weekly
                         Response of SPREAD_JP to RISK Innovation                            Response of SPREAD_SZ to RISK Innovation

       .028
       .024                                                                     .03
       .020
       .016                                                                     .02
       .012
       .008                                                                     .01
       .004
       .000                                                                     .00

    -.004
                    5         10    15       20    25     30         35    40          5       10      15        20    25      30         35    40




   •          Monthly
                        Response of SPREAD_JP to RISK Innovation                             Response of SPREAD_SZ to RISK Innovation

    .12
                                                                                .10
    .10
                                                                                .08
    .08                                                                         .06
    .06                                                                         .04
                                                                                .02
    .04
                                                                                .00
    .02
                                                                                -.02
    .00                                                                         -.04
                5         10       15        20   25      30         35   40           5        10     15        20    25      30         35    40




                                                                            32
ADBI Working Paper 1345                                                                                                                                                  Beirne and Sugandi



          Figure A4.5: Equity Market Responses to Risk-off Shocks in Safe Havens
         •          Daily
        Response of LOG(STOCK_IDX_JP) to RISK Innovation                         Response of LOG(STOCK_IDX_SZ) to RISK Innovation                          Response of LOG(STOCK_IDX_US) to RISK Innovation

                                                                        .0020                                                                     .0010
.002
                                                                        .0015                                                                     .0005
.001                                                                    .0010                                                                     .0000
                                                                        .0005                                                                     -.0005
.000
                                                                        .0000                                                                     -.0010
-.001                                                                   -.0005                                                                    -.0015
                                                                        -.0010                                                                    -.0020
-.002
                                                                        -.0015                                                                    -.0025
                   25             50        75        100         125                       25            50        75           100        125                   25            50        75           100        125




         •          Weekly
               Response of LOG(STOCK_IDX_JP) to RISK Innovation                        Response of LOG(STOCK_IDX_SZ) to RISK Innovation                      Response of LOG(STOCK_IDX_US) to RISK Innovation

                                                                                                                                                  .003
.002                                                                    .002
                                                                                                                                                  .002
                                                                        .001                                                                      .001
.000
                                                                        .000                                                                      .000
-.002                                                                   -.001                                                                     -.001
                                                                        -.002                                                                     -.002
-.004
                                                                        -.003                                                                     -.003
-.006                                                                   -.004                                                                     -.004
                                                                                                                                                  -.005
                                                                        -.005
           5         10      15        20    25     30      35     40              5         10      15        20    25     30         35    40              5     10      15        20   25      30         35    40




         •          Monthly
             Response of LOG(STOCK_IDX_JP) to RISK Innovation                      Response of LOG(STOCK_IDX_SZ) to RISK Innovation                          Response of LOG(STOCK_IDX_US) to RISK Innovation

.005                                                                                                                                              .000
                                                                        .004
.000                                                                    .000                                                                      -.005
-.005                                                                   -.004
                                                                        -.008                                                                     -.010
-.010
                                                                        -.012                                                                     -.015
-.015                                                                   -.016
-.020                                                                   -.020                                                                     -.020
                                                                        -.024
-.025                                                                                                                                             -.025
                                                                        -.028
           5         10      15        20    25     30      35     40              5         10      15        20    25     30         35    40              5     10      15        20   25      30         35    40




                                                                                                           33
ADBI Working Paper 1345                                                                                                                                            Beirne and Sugandi



       Figure A4.6: Portfolio Debt Flow Responses to Risk-off Shocks in Safe Havens
        •         Daily
             Response of DEBTSEC_JP to RISK Innovation                            Response of DEBTSEC_SZ to RISK Innovation                             Response of DEBTSEC_US to RISK Innovation

.015
                                                                        .00                                                                  .020
.010
                                                                       -.01                                                                  .016
.005
                                                                       -.02                                                                  .012
.000
                                                                       -.03                                                                  .008
-.005
                                                                       -.04                                                                  .004
-.010
                                                                       -.05                                                                  .000
-.015
                 25           50        75            100        125                  25            50        75            100        125                 25             50        75           100        125




        •         Weekly
               Response of DEBTSEC_JP to RISK Innovation                             Response of DEBTSEC_SZ to RISK Innovation                            Response of DEBTSEC_US to RISK Innovation

                                                                       .02                                                                   .04
.04
                                                                       .00
                                                                                                                                             .03
.03
                                                                       -.02
.02                                                                    -.04                                                                  .02
.01                                                                    -.06
                                                                                                                                             .01
.00                                                                    -.08
-.01                                                                   -.10                                                                  .00

-.02                                                                   -.12
         5        10     15        20    25      30         35    40          5        10      15        20    25      30         35    40          5        10     15         20   25      30         35    40




        •         Monthly
               Response of DEBTSEC_JP to RISK Innovation                            Response of DEBTSEC_SZ to RISK Innovation                             Response of DEBTSEC_US to RISK Innovation

                                                                                                                                             .08
                                                                       .1
.10                                                                                                                                          .06
                                                                       .0                                                                    .04
.05                                                                                                                                          .02
                                                                       -.1
                                                                                                                                             .00
.00                                                                    -.2                                                                   -.02
                                                                                                                                             -.04
-.05                                                                   -.3
                                                                                                                                             -.06
                                                                       -.4                                                                   -.08
         5        10     15        20    25      30         35    40          5        10      15        20    25      30         35    40          5        10      15        20    25     30         35    40




                                                                                                         34
ADBI Working Paper 1345                                                                                                                                        Beirne and Sugandi



 Figure A4.7: Portfolio Equity Flow Responses to Risk-off Shocks in Safe Havens
        •       Daily
            Response of EQUITY_JP to RISK Innovation                           Response of EQUITY_SZ to RISK Innovation                              Response of EQUITY_US to RISK Innovation

                                                                    .06
.005                                                                                                                                      .012
                                                                    .05
.000                                                                .04                                                                   .008
-.005                                                               .03
                                                                                                                                          .004
                                                                    .02
-.010
                                                                    .01                                                                   .000
-.015
                                                                    .00                                                                  -.004
               25            50        75         100         125                 25             50        75         100          125                  25            50        75           100        125




        •       Weekly
              Response of EQUITY_JP to RISK Innovation                             Response of EQUITY_SZ to RISK Innovation                           Response of EQUITY_US to RISK Innovation

                                                                    .14                                                                  .03
.02
                                                                    .12
.01                                                                 .10                                                                  .02
                                                                    .08
.00
                                                                    .06                                                                  .01
-.01                                                                .04
                                                                    .02                                                                  .00
-.02
                                                                    .00
                                                                    -.02                                                                 -.01
        5       10      15        20    25      30       35    40          5           10    15       20     25      30       35    40           5       10      15        20    25     30         35    40




        •       Monthly
              Response of EQUITY_JP to RISK Innovation                            Response of EQUITY_SZ to RISK Innovation                             Response of EQUITY_US to RISK Innovation

                                                                    .5
                                                                                                                                         .08
.04                                                                 .4
                                                                                                                                         .06
.00                                                                 .3
                                                                                                                                         .04
-.04                                                                .2
                                                                                                                                         .02
                                                                    .1
-.08                                                                                                                                     .00
                                                                    .0
-.12                                                                                                                                     -.02
                                                                    -.1
                                                                                                                                         -.04
        5       10      15        20    25      30       35    40          5        10      15        20    25      30        35    40           5       10      15        20    25     30         35    40




                                                                                                      35
