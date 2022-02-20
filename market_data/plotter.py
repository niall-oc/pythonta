#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:02:46 2021

@author: xual
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

class Plotter:

    def __init__(self, mkt_data):
        self.mkt_data = mkt_data
        self.title = f"{self.mkt_data.symbol} {self.mkt_data.interval}"
        self.harmonics = None
        self.divergences = None
        self.VOLUME_ROW = 2
        self.MACD_ROW = 3
        self.RSI_ROW = 4
        self.MFI_ROW = 5
        self.ROW_MAP = {
            'macd': self.MACD_ROW,
            'volume': self.VOLUME_ROW,
            'rsi': self.RSI_ROW,
            'mfi': self.MFI_ROW
        }
        self.set_main_plot()
        self.colors = { 
            'bearish': {
                'formed': {
                    'line' : 'rgba(255, 127, 0, 0.6)',
                    'fill': 'rgba(255, 127, 0, 0.2)'
                },
                'forming': {
                    'line': 'rgba(200, 0, 200, 0.6)',
                    'fill': 'rgba(200, 0, 200, 0.2)'
                }
            },
            'bullish': {
                'formed': {
                    'line' : 'rgba(0, 255, 0, 0.6)',
                    'fill': 'rgba(0, 255, 0, 0.2)'
                },
                'forming': {
                    'line': 'rgba(200, 200, 0, 0.6)',
                    'fill': 'rgba(200, 200, 0, 0.2)'
                }
            }
        }
        
    def set_main_plot(self):
        self.main_plot = make_subplots(
            rows=6, cols=1, shared_xaxes=True,
            vertical_spacing=0.01, 
            row_heights=[0.5,0.1,0.1,0.1,0.1,0.1]
        )
        self.main_plot.add_trace(
            go.Candlestick(
                x=self.mkt_data.df.index,
                open=self.mkt_data.df[self.mkt_data.OPEN],
                high=self.mkt_data.df[self.mkt_data.HIGH],
                close=self.mkt_data.df[self.mkt_data.CLOSE],
                low=self.mkt_data.df[self.mkt_data.LOW],
            )
        )
        
        self.main_plot.update_yaxes(title_text=f"{self.mkt_data.symbol} {self.mkt_data.interval} Price", row=1, col=1)
        # Plot volume trace on 2nd row
        colors = ['lightgreen' if row[self.mkt_data.OPEN] - row[self.mkt_data.CLOSE] >= 0 else '#ff7766' 
                  for index, row in self.mkt_data.df.iterrows()]
        self.main_plot.add_trace(
            go.Bar(
                x=self.mkt_data.df.index, 
                y=self.mkt_data.df[self.mkt_data.VOLUME],
                marker_color=colors
            ), 
            row=2, col=1
        )
        self.main_plot.update_yaxes(title_text="Volume", row=2, col=1)
        # Plot MACD trace on 3rd row
        self.plot_row = 2
        if self.mkt_data.macd:
            self.plot_row += 1
            colors = ['lightgreen' if val >= 0 else '#ff7766' for val in self.mkt_data.macd.macd_diff()]
            self.main_plot.add_trace(go.Bar(x=self.mkt_data.df.index, 
                                 y=self.mkt_data.macd.macd_diff(),
                                 marker_color=colors
                                ), row=self.plot_row, col=1)
            # MACD Diff is enough for divergences
            #self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
            #                         y=self.mkt_data.macd.macd(),
            #                         line=dict(color='yellow', width=2)
            #                        ), row=3, col=1)
            #self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
            #                         y=self.mkt_data.macd.macd_signal(),
            #                         line=dict(color='pink', width=1)
            #                        ), row=3, col=1)
            self.main_plot.update_yaxes(title_text="MACD", showgrid=False, row=self.plot_row, col=1)
        if self.mkt_data.rsi:
            self.plot_row += 1
            # Plot stochastics trace on 4th row
            self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
                                     y=self.mkt_data.rsi.rsi(),
                                     line=dict(color='yellow', width=2)
                                    ), row=self.plot_row, col=1)
            self.main_plot.update_yaxes(title_text="RSI", row=self.plot_row, col=1)
        if self.mkt_data.mfi:
            self.plot_row += 1
            # Plot stochastics trace on 4th row
            self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
                                     y=self.mkt_data.mfi.chaikin_money_flow(),
                                     line=dict(color='cyan', width=2)
                                    ), row=self.plot_row, col=1)
            self.main_plot.update_yaxes(title_text="MFI", row=self.plot_row, col=1)
            
    def add_harmonic_plots(self, harmonics):
        self.title = f"{self.title}  -  {len(harmonics)} harmonics"
        for h in harmonics:                
            if len(h['peak_indexes']) == 5:
                # 5 point m or w formations
                text = [f'X {h["peak_prices"][0]}', f'A {str(h["type"])}', f"B {h['retraces']['XAB']:0.3f}", f"C {h['retraces']['ABC']:0.3f}", f"D {h['retraces']['XAD']:0.3f}"]
                lt = h['peak_indexes'][0:3]+h['peak_indexes'][:1]
                rt = h['peak_indexes'][2:]+h['peak_indexes'][2:3]
                lp = h['peak_prices'][0:3]+h['peak_prices'][:1]
                rp = h['peak_prices'][2:]+h['peak_prices'][2:3]
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+markers+text",
                        x=self.mkt_data.df.index.values[lt],
                        y=lp,
                        fill="toself",
                        fillcolor=self.colors[h['direction']][h['stage']]['fill'],
                        line=dict(color=self.colors[h['direction']][h['stage']]['line'], width=2),
                        text=text[0:3],
                        textposition="top center"
                    )
                )
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+markers+text",
                        x=self.mkt_data.df.index.values[rt],
                        y=rp,
                        fill="toself",
                        fillcolor=self.colors[h['direction']][h['stage']]['fill'],
                        line=dict(color=self.colors[h['direction']][h['stage']]['line'], width=2),
                        text=text[2:],
                        textposition="top center"
                    )
                )
            else:
                # 4 point ABCD drives
                text = [f"A {h['peak_prices'][0]:.3f} ABCD", f"B {h['peak_prices'][1]:.3f}", f"C {h['retraces']['ABC']:0.3f}", f"D {h['retraces']['BCD']:0.3f}"]
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+text",
                        x=self.mkt_data.df.index.values[h['peak_indexes']],
                        y=h['peak_prices'],
                        line=dict(color=self.colors[h['direction']][h['stage']]['line'], width=4),
                        text=text,
                        textposition="top center"
                    )
                )
    
    def add_head_shoulders_plots(self, head_shoulders):
        """
        """
        self.title = f"{self.title}  -  {len(head_shoulders)} head&shoulders"
        for h in head_shoulders:
            if h['direction'] == 'bearish':
                color = 'rgba(255, 127, 0, 0.3)' if h['stage'] == 'formed' else 'rgba(200, 0, 200, 0.3)'
            else:
                color = 'rgba(0, 255, 0, 0.3)' if h['stage'] == 'formed' else 'rgba(200, 200, 0, 0.3)'
                
            self.main_plot.add_trace(
                go.Scatter(
                    mode="lines+markers+text",
                    x=self.mkt_data.df.index.values[h['peak_indexes']],
                    y=h['peak_prices'],
                    #fill="toself",
                    line=dict(color=color, width=2),
                    #text=text[0:3],
                    #textposition="top center"
                )
            )

    def add_divergence_plots(self, divergences):
        for d in divergences:
            color = '#ff7766' if d['direction'] == 'bearish' else 'lightgreen'
            row = self.ROW_MAP[d['type']]
            self.main_plot.add_trace(
                go.Scatter(
                    mode="lines+markers",
                    x=self.mkt_data.df.index.values[d['peak_indexes']],
                    y=d['peak_prices'],
                    line=dict(color=color, width=2)
                ), row=row, col=1
            )
   
    def add_peaks(self, harmonics):
        self.main_plot.add_trace(
            go.Scatter(
                    mode="markers",
                    x=self.mkt_data.df.index.values[harmonics.peak_indexes],
                    y=harmonics.peak_prices,
                    line=dict(color='white', width=2)
                )
            )
    def add_obs(self, obs_values):
        self.plot_row += 1
        self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
                                     y=obs_values,
                                 line=dict(color='orange', width=2)
                                ), row=self.plot_row, col=1)
        self.main_plot.update_yaxes(title_text="OBS", row=self.plot_row, col=1)
    
    def add_indicator_signals(self, signals):
        for name, details in signals.items():
            color = 'lightgreen'
            s = details['bullish']
            self.main_plot.add_trace(
                go.Scatter(
                    mode="markers",
                    x=self.mkt_data.df.index.values[s['idx']],
                    y=s['peak_prices'],
                    text=f"{name}-buy",
                    line=dict(color=color, width=2)
                )
            )
            s = details['bearish']
            color = 'rgba(255, 144, 50, 0.1)'
            self.main_plot.add_trace(
                go.Scatter(
                    mode="markers",
                    x=self.mkt_data.df.index.values[s['idx']],
                    y=s['peak_prices'],
                    line=dict(color=color, width=2)
                )
            )
    
    def save_plot_image(self, location, yahoo=False):
        self.main_plot.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=False,
            font=dict(
                family="Courier New, monospace",
                size=18
            ),
            title={
                'text': self.title,
                'y':0.96,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            title_font_size=38
        )
        if yahoo:
            self.main_plot.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]), #hide weekends
                    dict(values=["2015-12-25", "2016-01-01"]),  # hide Christmas and New Year's
                    dict(bounds=[16, 9.5], pattern="hour")
                ]
            )
        pio.write_image(self.main_plot, f"{location}", width=6*600, height=3*600, scale=1)