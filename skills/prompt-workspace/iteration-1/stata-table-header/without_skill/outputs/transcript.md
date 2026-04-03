Understood. You want the "second layer" descriptors (e.g., the exposure measure used, the sample definition, the dependent variable category) moved from the bottom of the table to near the top, appearing as the second or third header line, consistent with the reference model.

In practice, this means restructuring the `esttab` call so that these labels appear in `prefoot()` or, better, in `prehead()` / `posthead()` rather than in `prefoot()` or the note block.

Here is what the change looks like concretely.

**Before (exposure info buried at the bottom):**

```stata
esttab ... ///
    prehead("\begin{tabular}{l*{6}{c}}" "\hline\hline") ///
    posthead("\hline") ///
    prefoot("\hline") ///
    postfoot( ///
        "\hline\hline" ///
        "\multicolumn{7}{l}{\footnotesize Exposure: County-level}" "\\" ///
        "\end{tabular}" ///
    )
```

This produces a table where "Exposure: County-level" only shows up at the very bottom, after all coefficients and statistics.

**After (exposure info as second/third header line):**

```stata
esttab ... ///
    prehead("\begin{tabular}{l*{6}{c}}" "\hline\hline") ///
    posthead( ///
        "\multicolumn{7}{l}{\footnotesize Exposure: County-level}" "\\" ///
        "\hline" ///
    ) ///
    prefoot("\hline") ///
    postfoot("\hline\hline" "\end{tabular}")
```

Now "Exposure: County-level" appears right after the column headers and before the coefficient rows, exactly as in the reference model.

If there are multiple descriptor lines (e.g., exposure + sample), stack them:

```stata
    posthead( ///
        "\multicolumn{7}{l}{\footnotesize Exposure: County-level}" "\\" ///
        "\multicolumn{7}{l}{\footnotesize Sample: Manufacturing firms}" "\\" ///
        "\hline" ///
    ) ///
```

To apply this: point me to the do-file that generates the table and I will move the relevant lines from `postfoot`/`prefoot` into `posthead`, keeping everything else intact.
