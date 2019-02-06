
# 使い方

`IEEEtranS_withJP.bst`というファイルをPathの通った箇所かtexファイルと同じフォルダに入れて，以下のように文章内で記述する。（`ref.bib`は自分で作ったbibファイルを参照するように。）

```tex
\bibliographystyle{IEEEtranS_withJP}
\bibliography{ref.bib}
```



# 変更箇所
[参考文献](https://qiita.com/HexagramNM/items/3ad757a9f5ee5d15e363#_reference-2be0cc9a71381591bb17)の記述をもとに[元ファイルIEEEtranS.bst](http://tug.ctan.org/tex-archive/macros/latex/contrib/IEEEtran/bibtex/IEEEtranS.bst)を変更しました。

詳しく書いてないところは参考文献の丸写しということなのでそちらを参照あれ。

## 日本語のみフルネーム表記へと変更する下準備

`FUNCTION {default.name.format.string}{ "{f.~}{vv~}{ll}{, jj}" }`のうち，`{f.~}`がデフォルトの名前の表記を名字1文字+カンマに設定しています。これを以下のように`{ff~}`と変更すれば，名字をフルネームで書けるようになります。
`FUNCTION {default.name.format.string}{ "{ff~}{vv~}{ll}{, jj}" } }`


しかし，これはデフォルトの設定を変えてしまうので英語のフォーマットを崩してしまいます。後の行を見ると実はinitializeの過程で`name.format.string`にこれを代入しているに過ぎません。ということで，後に追加する`japanese.flag`に応じてこれを変更するように書けばよいわけです。


```
FUNCTION {initialize.controls}
{ default.is.use.number.for.article 'is.use.number.for.article :=
  default.is.use.paper 'is.use.paper :=
  default.is.use.url 'is.use.url :=
  default.is.forced.et.al 'is.forced.et.al :=
  default.max.num.names.before.forced.et.al 'max.num.names.before.forced.et.al :=
  default.num.names.shown.with.forced.et.al 'num.names.shown.with.forced.et.al :=
  default.is.use.alt.interword.spacing 'is.use.alt.interword.spacing :=
  default.is.dash.repeated.names 'is.dash.repeated.names :=
  default.ALTinterwordstretchfactor 'ALTinterwordstretchfactor :=
  default.name.format.string 'name.format.string :=
  default.name.latex.cmd 'name.latex.cmd :=
  default.name.url.prefix 'name.url.prefix :=
}
```

従って私の手法では，とりあえず次のように別の変数を立てるようにします。

```
% The default name format control string. %change based on japanese
FUNCTION {default.name.format.string}{ "{f.~}{vv~}{ll}{, jj}" }
FUNCTION {default.name.format.string.forJP}{ "{ff~}{vv~}{ll}{, jj}" } %%追加箇所
```




## フラグの追加

- bibファイルにisjapaneseフラグを追加。
- bstファイル内でフラグを管理するInteger`japanese.flag`に関する記述を追加。



## 日本語文献のカンマやピリオドの全角化，"の後にカンマが来るように変更
`FUNCTION {output.nonnull}`と` FUNCTION {fin.entry}`を変更。


## 日本語文献の複数著者の場合に出てきてしまうandの抑制
`FUNCTION{format.names}`の変更。

## 全ての文献形式にフラグを管理する処理を追加 + 日本語
bibにisjapaneseが{true}で入っていた場合に`japanese.flag`を立てる処理をします。
また，先程述べた日本語と英語での書式の変更もここでやってしまいます。

`isjapanese`を探して`japanese.flag`を立てる他，日本語用の名前フォーマット`default.name.format.string.forJP`
へと`name.format.string`を切り替えます。

```
FUNCTION {article}
{ std.status.using.comma
  start.entry
  %%変更箇所1：日本語エントリに何かあれば日本語化するフラグを立てる
  isjapanese empty$ 
   {skip$} 
   {#1 'japanese.flag :=
   default.name.format.string.forJP 'name.format.string :=} 
 if$ 
  %%変更箇所1ここまで
  if.url.alt.interword.spacing
  format.authors "author" output.warn
  name.or.dash
  format.article.title "title" output.warn
  format.journal "journal" bibinfo.check "journal" output.warn
  format.volume output
  format.number.if.use.for.article output
  format.pages output
  format.date "year" output.warn
  format.note output
  format.url output
  fin.entry
  if.url.std.interword.spacing
  %%変更箇所2：次の文献のために日本語化フラグの解除(0に戻しておく)
  #0 'japanese.flag :=
  default.name.format.string 'name.format.string :=
  %%変更箇所2ここまで
}
```

これを全ての処理に適用します。

### 一括置換したときのメモ
たくさんあったので以下の正規表現置換を使用しました。
ただし，変換後に\nが素の文書で出たり，エスケープを書き忘れたり等ミスが多いので結局人力でコピペしてもいいかもしれない…
そして置換内容が古いのでただのlogと思ってくださいorz

置換前

```
start.entry\n  if.url
```

置換後

```
start.entry\n  %%変更箇所1：日本語エントリに何かあれば日本語化するフラグを立てる\n  isjapanese empty$ \n   {skip$} \n   {#1 'japanese.flag :=} \n if$ \n  %%変更箇所1ここまで\n  if.url
```

置換前

```
if.url.std.interword.spacing\n}
```

置換後

```
if.url.std.interword.spacing\n  %%変更箇所2：次の文献のために日本語化フラグの解除(0に戻しておく)\n  #0 'japanese.flag :=\n  %%変更箇所2ここまで\n}
```