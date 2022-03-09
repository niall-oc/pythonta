#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 17:02:46 2021

@author: xual
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

from market_data.market_data_base import MktDataBase

class Plotter:

    def __init__(self, mkt_data, yahoo=False, row_map=None, colors=None):
        self.mkt_data = mkt_data
        self.title = f"{self.mkt_data.symbol} {self.mkt_data.interval}"
        self.harmonics = None
        self.divergences = None
        self.is_yahoo=yahoo
        self.ROW_MAP = row_map or {
            'macd': 3,
            'volume': 2,
            'rsi': 4,
            'mfi': 5,
            'obs': 6
        }
        self.set_main_plot()
        self.colors = colors or { 
            'bearish': {
                True: { # formed
                    'line' : 'rgba(255, 127, 0, 0.6)',
                    'fill': 'rgba(255, 127, 0, 0.2)'
                },
                False: { # forming
                    'line': 'rgba(200, 0, 200, 0.6)',
                    'fill': 'rgba(200, 0, 200, 0.2)'
                }
            },
            'bullish': {
                True: { # formed
                    'line' : 'rgba(0, 255, 0, 0.6)',
                    'fill': 'rgba(0, 255, 0, 0.2)'
                },
                False: { # forming
                    'line': 'rgba(200, 200, 0, 0.6)',
                    'fill': 'rgba(200, 200, 0, 0.2)'
                }
            }
        }
        
    def set_main_plot(self, yahoo=False):
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
            row=self.ROW_MAP['volume'], col=1
        )
        self.main_plot.update_yaxes(title_text="Volume", row=2, col=1)
        # Plot MACD trace on 3rd row
        if self.mkt_data.macd:
            colors = ['lightgreen' if val >= 0 else '#ff7766' for val in self.mkt_data.macd.macd_diff()]
            self.main_plot.add_trace(go.Bar(x=self.mkt_data.df.index, 
                                 y=self.mkt_data.macd.macd_diff(),
                                 marker_color=colors
                                ), row=self.ROW_MAP['macd'], col=1)
            # MACD Diff is enough for divergences
            #self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
            #                         y=self.mkt_data.macd.macd(),
            #                         line=dict(color='yellow', width=2)
            #                        ), row=3, col=1)
            #self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
            #                         y=self.mkt_data.macd.macd_signal(),
            #                         line=dict(color='pink', width=1)
            #                        ), row=3, col=1)
            self.main_plot.update_yaxes(title_text="MACD", showgrid=False, row=self.ROW_MAP['macd'], col=1)
        if self.mkt_data.rsi:
            # Plot stochastics trace on 4th row
            self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
                                     y=self.mkt_data.rsi.rsi(),
                                     line=dict(color='yellow', width=2)
                                    ), row=self.ROW_MAP['rsi'], col=1)
            self.main_plot.update_yaxes(title_text="RSI", row=self.ROW_MAP['rsi'], col=1)
        if self.mkt_data.mfi:
            # Plot stochastics trace on 4th row
            self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
                                     y=self.mkt_data.mfi.chaikin_money_flow(),
                                     line=dict(color='cyan', width=2)
                                    ), row=self.ROW_MAP['mfi'], col=1)
            self.main_plot.update_yaxes(title_text="MFI", row=self.ROW_MAP['mfi'], col=1)

    def add_harmonic_plots(self, patterns):
        self.title = f"{self.title}  -  {len(patterns)} harmonics"
        for p in patterns:                
            if len(p.idx) == 5:
                # 5 point m or w formations
                text = [f'X {p.y[0]}', f'A {p.name}', f"B {p.retraces['XAB']:0.3f}", f"C {p.retraces['ABC']:0.3f}", f"D {p.retraces['XAD']:0.3f}"]
                lt = p.idx[0:3]+p.idx[:1]
                rt = p.idx[2:]+p.idx[2:3]
                lp = p.y[0:3]+p.y[:1]
                rp = p.y[2:]+p.y[2:3]
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+markers+text",
                        x=self.mkt_data.df.index.values[lt],
                        y=lp,
                        fill="toself",
                        fillcolor=self.colors[p.direction][p.formed]['fill'],
                        line=dict(color=self.colors[p.direction][p.formed]['line'], width=2),
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
                        fillcolor=self.colors[p.direction][p.formed]['fill'],
                        line=dict(color=self.colors[p.direction][p.formed]['line'], width=2),
                        text=text[2:],
                        textposition="top center"
                    )
                )
            else:
                # 4 point ABCD drives
                text = [f"A {p.y[0]:.3f} ABCD", f"B {p.y[1]:.3f}", f"C {p.retraces['ABC']:0.3f}", f"D {p.retraces['BCD']:0.3f}"]
                self.main_plot.add_trace(
                    go.Scatter(
                        mode="lines+text",
                        x=self.mkt_data.df.index.values[p.idx],
                        y=p.y,
                        line=dict(color=self.colors[p.direction][p.formed]['line'], width=4),
                        text=text,
                        textposition="top center"
                    )
                )
    
    def add_head_shoulders_plots(self, patterns):
        """
        """
        self.title = f"{self.title}  -  {len(patterns)} head&shoulders"
        for p in patterns:
            if p.direction == 'bearish':
                color = 'rgba(255, 127, 0, 0.3)' if p.formed else 'rgba(200, 0, 200, 0.3)'
            else:
                color = 'rgba(0, 255, 0, 0.3)' if p.formed else 'rgba(200, 200, 0, 0.3)'
                
            self.main_plot.add_trace(
                go.Scatter(
                    mode="lines+markers+text",
                    x=self.mkt_data.df.index.values[p.idx],
                    y=p.y,
                    #fill="toself",
                    line=dict(color=color, width=2),
                    #text=text[0:3],
                    #textposition="top center"
                )
            )

    def add_divergence_plots(self, patterns):
        for p in patterns:
            color = '#ff7766' if p.direction == 'bearish' else 'lightgreen'
            self.main_plot.add_trace(
                go.Scatter(
                    mode="lines+markers",
                    x=self.mkt_data.df.index.values[p.idx],
                    y=p.y,
                    line=dict(color=color, width=2)
                ), row=self.ROW_MAP[p.derived_from], col=1
            )
   
    def add_peaks(self, taobject):
        self.main_plot.add_trace(
            go.Scatter(
                    mode="markers",
                    x=self.mkt_data.df.index.values[taobject.peak_indexes],
                    y=taobject.peak_prices,
                    line=dict(color='lightgrey', width=2)
                )
            )
    
    def add_obs(self, obs_values):
        self.main_plot.add_trace(go.Scatter(x=self.mkt_data.df.index,
                                     y=obs_values,
                                 line=dict(color='orange', width=2)
                                ), row=self.ROW_MAP['obs'], col=1)
        self.main_plot.update_yaxes(title_text="OBS", row=self.ROW_MAP['obs'], col=1)
    
    def save_plot_image(self, location):
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
        pio.write_image(self.main_plot, f"{location}", width=6*600, height=3*600, scale=1)