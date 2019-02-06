
# 使い方

`IEEEtranS_withJP.bst`というファイルをPathの通った箇所かtexファイルと同じフォルダに入れて，以下のように文章内で記述する。（`ref.bib`は自分で作ったbibファイルを参照するように。）

```tex
\bibliographystyle{IEEEtranS_withJP}
\bibliography{ref.bib}
```

# 参考にした文献


# 変更箇所

## フルネーム表記へと変更

```
% The default name format control string. %change based on japanese
#1 japanese.flag =
  { FUNCTION {default.name.format.string}{ "{ff~}{vv~}{ll}{, jj}" } }
  { FUNCTION {default.name.format.string}{ "{f.~}{vv~}{ll}{, jj}" } }
if$
```

## 