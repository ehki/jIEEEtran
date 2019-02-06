
# 使い方

`IEEEtranS_withJP.bst`というファイルをPathの通った箇所かtexファイルと同じフォルダに入れて，以下のように文章内で記述する。（`ref.bib`は自分で作ったbibファイルを参照するように。）

```tex
\bibliographystyle{IEEEtranS_withJP}
\bibliography{ref.bib}
```



# 変更箇所
[参考文献](https://qiita.com/HexagramNM/items/3ad757a9f5ee5d15e363#_reference-2be0cc9a71381591bb17)の記述をもとに[元ファイルIEEEtranS.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtranS.bst)を変更。

## フルネーム表記へと変更

```
% The default name format control string. %change based on japanese
#1 japanese.flag =
  { FUNCTION {default.name.format.string}{ "{ff~}{vv~}{ll}{, jj}" } }
  { FUNCTION {default.name.format.string}{ "{f.~}{vv~}{ll}{, jj}" } }
if$
```
## フラグの追加

- bibファイルにisjapaneseフラグを追加。
- bstファイル内でフラグを管理するInteger`japanese.flag`に関する記述を追加。



## 日本語文献のカンマやピリオドの全角化，"の後にカンマが来るように変更
`FUNCTION {output.nonnull}`と` FUNCTION {fin.entry}`を変更



## 日本語文献の複数著者の場合に出てきてしまうandの抑制
`FUNCTION{format.names}`の変更

## 全ての文献形式にフラグを管理する処理を追加
bibにisjapaneseが{true}で入っていた場合にjapanese.flagを立てる処理。
たくさんあったので以下の正規表現置換を使用。

置換前

```
start.entry\n  if.url
```

置換後

```
start.entry\n  %%変更箇所1：日本語エントリに何かあれば日本語化するフラグを立てる\n  isjapanese empty$ \n   {skip$} \n   {#1 'japanese.flag :=} \n if$\n  %%変更箇所1ここまで\n  if.url
```

置換前

```
if.url.std.interword.spacing\n}
```

置換後

```
if.url.std.interword.spacing\n  %%変更箇所2：次の文献のために日本語化フラグの解除(0に戻しておく)\n  #0 'japanese.flag :=\n  %%変更箇所2ここまで\n}
```